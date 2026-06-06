"""
scripts/generate_oracle_dataset.py

Builds a verified dataset using the execution oracle approach:

  1. Loads MBPP problems with their test cases
     (local .jsonl file via --mbpp-path, HuggingFace `datasets`, or bundled 20-problem subset)
  2. For each problem generates three code variants via a local Ollama model:
       direct        — honest attempt at the solution  (target: VALID)
       hallucinated  — instructed to use a nonexistent library (target: HALLUCINATION)
       grounded_err  — instructed to make an API-usage mistake (target: GROUNDED_ERROR)
  3. Executes each snippet against the test assertions in a subprocess with timeout
  4. Labels each sample from the execution result (not the generation strategy),
     giving verified ground truth with zero manual review
  5. Writes results/dataset_oracle_<N>problems.json

The prompt always includes the expected function name extracted from the first test
assertion, so models know what name to use.  This prevents the common failure mode
where a correct solution is labelled HALLUCINATION only because the model chose a
different function name.

Balancing improvements over v1
-------------------------------
  --retries K   Per-strategy retry budget: each variant is regenerated up to K
                times until the oracle label matches the strategy's intended label.
                This dramatically reduces the 85 % HALLUCINATION skew caused by
                direct solutions being labelled HALLUCINATION on the first attempt.

  --balance     Post-hoc resampling: after all samples are collected, undersample
                the majority classes so that all three labels have equal (or near-
                equal) representation.  Use with --target-each N to set a hard cap.

  --target-each N
                Target number of samples per label in the balanced output.
                Defaults to the size of the smallest observed class.

Usage
-----
    python scripts/generate_oracle_dataset.py
    python scripts/generate_oracle_dataset.py --mbpp-path "D:/MBPP/mbpp.jsonl" --problems 100
    python scripts/generate_oracle_dataset.py --problems 50 --model llama3
    python scripts/generate_oracle_dataset.py --problems 40 --retries 3 --balance
    python scripts/generate_oracle_dataset.py --problems 20 --output my_oracle.json

Flags
-----
  --mbpp-path PATH  Local MBPP .jsonl file (highest priority loader)
  --problems N      MBPP problems to use (default: 20; each yields up to 3 samples)
  --model           qwen (default) | llama3
  --retries K       Max regeneration attempts per strategy/problem pair (default: 1)
  --balance         Undersample majority classes for equal label distribution
  --target-each N   Samples per label in balanced output (default: min class size)
  --output PATH     Override the output path

Requirements
------------
  Ollama must be running on localhost:11434 with the chosen model pulled.
  --mbpp-path gives access to all 974 MBPP problems locally.
  Without it, `pip install datasets` enables full MBPP via HuggingFace; otherwise
  the script uses the bundled 20-problem subset automatically.
"""
import argparse
import json
import os
import random
import re
import sys
import time
from collections import Counter
from typing import List, Optional

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)

from src.oracle_executor import (
    execute_code,
    LABEL_VALID,
    LABEL_HALLUCINATION,
    LABEL_GROUNDED_ERROR,
)


# ---------------------------------------------------------------------------
# Generation prompts
# ---------------------------------------------------------------------------

_PROMPT_DIRECT = (
    "Write a Python function to solve the problem below.\n"
    "The function MUST be named exactly `{fn_name}`.\n"
    "Return ONLY the raw Python code — no markdown fences, no explanation.\n\n"
    "Problem: {task}"
)

_PROMPT_HALLUCINATE = (
    "Write a Python function to solve the problem below.\n"
    "The function MUST be named exactly `{fn_name}`.\n"
    "You MUST import and use the `{fake_lib}` library for the core computation.\n"
    "Return ONLY the raw Python code — no markdown fences, no explanation.\n\n"
    "Problem: {task}"
)

_PROMPT_GROUNDED_ERROR = (
    "Write a Python function to solve the problem below.\n"
    "The function MUST be named exactly `{fn_name}`.\n"
    "Your solution must attempt to use the correct Python built-in functions or\n"
    "standard library but apply them with at least one of these mistakes:\n"
    "  - calling a method on the wrong built-in type\n"
    "  - passing a keyword argument that does not exist on the function\n"
    "  - passing the wrong number of arguments to a standard function\n"
    "Return ONLY the raw Python code — no markdown fences, no explanation.\n\n"
    "Problem: {task}"
)

# Plausible-sounding but nonexistent library names
_FAKE_LIBS = [
    "sortinglib", "mathtools", "pyhelpers", "datautils", "pymath",
    "listops", "numutils", "stringtools", "arraylib", "calctools",
    "pyalgo", "seqtools", "mathlib", "codeutils", "pystructs",
]


# ---------------------------------------------------------------------------
# Ollama code generation
# ---------------------------------------------------------------------------

def _call_ollama(prompt: str, model: str, temperature: float) -> str:
    import urllib.request
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": temperature, "num_predict": 400},
    }).encode("utf-8")
    req = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("message", {}).get("content", "")


def _extract_code(raw: str) -> str:
    """Strip markdown fences; return only the Python source."""
    raw = re.sub(r"```(?:python)?\n?(.*?)```", r"\1", raw, flags=re.DOTALL)
    return raw.strip()


# ---------------------------------------------------------------------------
# MBPP problem loader
# ---------------------------------------------------------------------------

def _extract_fn_name(tests: list) -> str:
    """
    Extract the expected function name from the first test assertion.

    e.g. "assert similar_elements((3, 4, 5, 6), ...) == (4, 5)"  →  "similar_elements"
    Falls back to "solution" if the pattern cannot be matched.
    """
    first = tests[0] if tests else ""
    m = re.match(r"assert\s+([A-Za-z_]\w*)\s*\(", first)
    return m.group(1) if m else "solution"


def _load_from_local_file(path: str, limit: int) -> list:
    """Load MBPP problems from a local .jsonl file."""
    problems = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if len(problems) >= limit:
                break
            item = json.loads(line)
            tests = item.get("test_list", [])
            if not tests:
                continue
            setup = item.get("test_setup_code", "").strip()
            if setup:
                tests = [setup] + tests
            problems.append({
                "id": f"mbpp_{item['task_id']}",
                "source": "MBPP",
                "source_id": str(item["task_id"]),
                "prompt": item["text"],
                "tests": tests,
            })
    print(f"[loader] {len(problems)} problems loaded from local file: {path}")
    return problems


def _load_problems(limit: int, local_path: Optional[str] = None) -> list:
    """
    Load MBPP problems, trying sources in priority order:
      1. Local .jsonl file (--mbpp-path)   — up to 974 problems
      2. HuggingFace datasets library       — full sanitized split
      3. Bundled 20-problem subset          — offline fallback
    Each dict has: id, source, source_id, prompt, tests (list[str]).
    """
    if local_path:
        try:
            return _load_from_local_file(local_path, limit)
        except Exception as e:
            print(f"[loader] Local file failed ({e}) — falling back to HuggingFace")

    try:
        from datasets import load_dataset  # type: ignore
        ds = load_dataset("google-research-datasets/mbpp", "sanitized", split="test")
        problems = []
        for item in ds:
            if len(problems) >= limit:
                break
            tests = item.get("test_list", [])
            if not tests:
                continue
            problems.append({
                "id": f"mbpp_{item['task_id']}",
                "source": "MBPP",
                "source_id": str(item["task_id"]),
                "prompt": item["text"],
                "tests": tests,
            })
        print(f"[loader] {len(problems)} problems loaded from HuggingFace MBPP")
        return problems
    except Exception as e:
        print(f"[loader] HuggingFace unavailable ({e}) — using bundled subset")
        return _BUNDLED[:limit]


# ---------------------------------------------------------------------------
# 20-problem bundled MBPP subset (offline fallback)
# ---------------------------------------------------------------------------

_BUNDLED = [
    {
        "id": "mbpp_2", "source": "MBPP", "source_id": "2",
        "prompt": "Write a function to find the similar elements from the given two lists.",
        "tests": [
            "assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)",
            "assert similar_elements((1, 2, 3, 4),(5, 4, 3, 7)) == (3, 4)",
            "assert similar_elements((11, 12, 14, 13),(17, 15, 14, 13)) == (13, 14)",
        ],
    },
    {
        "id": "mbpp_3", "source": "MBPP", "source_id": "3",
        "prompt": "Write a python function to identify non-prime numbers.",
        "tests": [
            "assert is_not_prime(2) == False",
            "assert is_not_prime(10) == True",
            "assert is_not_prime(35) == True",
        ],
    },
    {
        "id": "mbpp_4", "source": "MBPP", "source_id": "4",
        "prompt": "Write a function to find the largest integers from a given list using heap queue algorithm.",
        "tests": [
            "assert heap_queue_largest([25, 35, 22, 85, 14, 65, 75, 22, 58], 3) == [85, 75, 65]",
            "assert heap_queue_largest([25, 35, 22, 85, 14, 65, 75, 22, 58], 2) == [85, 75]",
            "assert heap_queue_largest([25, 35, 22, 85, 14, 65, 75, 22, 58], 5) == [85, 75, 65, 58, 35]",
        ],
    },
    {
        "id": "mbpp_7", "source": "MBPP", "source_id": "7",
        "prompt": "Write a function to find all words which are at least 4 characters long in a string.",
        "tests": [
            "assert find_char_long('Please move back to the front') == ['Please', 'move', 'back', 'front']",
            "assert find_char_long('Jing Eco and Recycling') == ['Jing', 'Recycling']",
            "assert find_char_long('Jhon Jhon was here') == ['Jhon', 'Jhon', 'here']",
        ],
    },
    {
        "id": "mbpp_8", "source": "MBPP", "source_id": "8",
        "prompt": "Write a function to find squares of individual elements in a list.",
        "tests": [
            "assert square_nums([1, 2, 3, 4, 5]) == [1, 4, 9, 16, 25]",
            "assert square_nums([10, 20, 30]) == [100, 400, 900]",
            "assert square_nums([12, 15]) == [144, 225]",
        ],
    },
    {
        "id": "mbpp_11", "source": "MBPP", "source_id": "11",
        "prompt": "Write a python function to remove first and last occurrence of a given character from the string.",
        "tests": [
            "assert remove_Occ('hello','l') == 'heo'",
            "assert remove_Occ('abcda','a') == 'bcd'",
            "assert remove_Occ('PHP','P') == 'H'",
        ],
    },
    {
        "id": "mbpp_12", "source": "MBPP", "source_id": "12",
        "prompt": "Write a function to sort a given matrix in ascending order according to the sum of its rows.",
        "tests": [
            "assert sort_matrix([[1, 2, 3], [2, 4, 5], [1, 1, 1]]) == [[1, 1, 1], [1, 2, 3], [2, 4, 5]]",
            "assert sort_matrix([[5, 8, 9], [6, 4, 3], [2, 1, 4]]) == [[2, 1, 4], [6, 4, 3], [5, 8, 9]]",
        ],
    },
    {
        "id": "mbpp_17", "source": "MBPP", "source_id": "17",
        "prompt": "Write a function to find the perimeter of a square.",
        "tests": [
            "assert square_perimeter(10) == 40",
            "assert square_perimeter(5) == 20",
            "assert square_perimeter(4) == 16",
        ],
    },
    {
        "id": "mbpp_18", "source": "MBPP", "source_id": "18",
        "prompt": "Write a function to remove characters from the first string which are present in the second string.",
        "tests": [
            "assert remove_dirty_chars('probasket', 'basket') == 'pro'",
            "assert remove_dirty_chars('language', 'age') == 'lngu'",
            "assert remove_dirty_chars('phone', 'one') == 'ph'",
        ],
    },
    {
        "id": "mbpp_19", "source": "MBPP", "source_id": "19",
        "prompt": "Write a function to find whether a given array of integers contains any duplicate element.",
        "tests": [
            "assert test_duplicate([1,2,3,4,5]) == False",
            "assert test_duplicate([1,2,3,4,4]) == True",
            "assert test_duplicate([1,1,2,2,3,3,4,4,5]) == True",
        ],
    },
    {
        "id": "mbpp_56", "source": "MBPP", "source_id": "56",
        "prompt": "Write a python function to check if a given number is one less than twice its reverse.",
        "tests": [
            "assert check(70) == False",
            "assert check(23) == False",
            "assert check(73) == True",
        ],
    },
    {
        "id": "mbpp_57", "source": "MBPP", "source_id": "57",
        "prompt": "Write a python function to find the largest number that can be formed with the given list of digits.",
        "tests": [
            "assert find_Max_Num([1, 2, 3]) == 321",
            "assert find_Max_Num([4, 5, 6, 1]) == 6541",
            "assert find_Max_Num([1, 2, 3, 9]) == 9321",
        ],
    },
    {
        "id": "mbpp_59", "source": "MBPP", "source_id": "59",
        "prompt": "Write a python function to find the nth item of the lucas series.",
        "tests": [
            "assert lucas_num(9) == 76",
            "assert lucas_num(4) == 7",
            "assert lucas_num(3) == 4",
        ],
    },
    {
        "id": "mbpp_61", "source": "MBPP", "source_id": "61",
        "prompt": "Write a python function to count the number of pairs whose sum is equal to 'sum'.",
        "tests": [
            "assert get_pairs_count([1, 5, 7, -1, 5], 5, 6) == 3",
            "assert get_pairs_count([1, 5, 7, -1], 4, 6) == 2",
            "assert get_pairs_count([1, 1, 1, 1], 4, 2) == 6",
        ],
    },
    {
        "id": "mbpp_6", "source": "MBPP", "source_id": "6",
        "prompt": "Write a python function to check whether two numbers differ at one bit position only or not.",
        "tests": [
            "assert differ_at_one_bit_pos(13, 9) == True",
            "assert differ_at_one_bit_pos(15, 8) == False",
            "assert differ_at_one_bit_pos(2, 3) == True",
        ],
    },
    {
        "id": "mbpp_14", "source": "MBPP", "source_id": "14",
        "prompt": "Write a python function to find the volume of a triangular prism.",
        "tests": [
            "assert find_Volume(10, 8, 6) == 240",
            "assert find_Volume(3, 2, 2) == 6",
            "assert find_Volume(1, 2, 1) == 1",
        ],
    },
    {
        "id": "mbpp_16", "source": "MBPP", "source_id": "16",
        "prompt": "Write a function that returns true if the input string contains sequences of lowercase letters joined with an underscore and false otherwise.",
        "tests": [
            "assert text_lowercase_underscore('aab_caa_bb') == True",
            "assert text_lowercase_underscore('aab_Caa_bb') == False",
            "assert text_lowercase_underscore('Aaab_caa_bb') == False",
        ],
    },
    {
        "id": "mbpp_20", "source": "MBPP", "source_id": "20",
        "prompt": "Write a function to check if the given number is woodball or not.",
        "tests": [
            "assert is_woodall(383) == True",
            "assert is_woodall(254) == False",
            "assert is_woodall(200) == False",
        ],
    },
    {
        "id": "mbpp_9", "source": "MBPP", "source_id": "9",
        "prompt": "Write a python function to find the minimum number of rotations required to get the same string.",
        "tests": [
            "assert find_Rotations('aaaa') == 1",
            "assert find_Rotations('ab') == 2",
            "assert find_Rotations('abc') == 3",
        ],
    },
    {
        "id": "mbpp_58", "source": "MBPP", "source_id": "58",
        "prompt": "Write a python function to count the number of substrings with the sum of digits equal to their length.",
        "tests": [
            "assert count_Substrings('112112', 3) == 1",
            "assert count_Substrings('111', 1) == 3",
            "assert count_Substrings('1101112', 3) == 1",
        ],
    },
]


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

# Maps each generation strategy to the oracle label it is designed to produce.
_STRATEGY_TARGET: dict = {
    "direct":       LABEL_VALID,
    "hallucinated": LABEL_HALLUCINATION,
    "grounded_err": LABEL_GROUNDED_ERROR,
}


def balance_samples(
    samples: List[dict],
    target_each: Optional[int] = None,
    seed: int = 42,
) -> List[dict]:
    """
    Undersample majority classes so all three labels have equal representation.

    Parameters
    ----------
    samples     : full unbalanced sample list
    target_each : desired samples per label; defaults to the smallest class size
    seed        : random seed for reproducibility

    Returns
    -------
    Balanced list (shuffled).
    """
    rng = random.Random(seed)
    by_label: dict = {LABEL_VALID: [], LABEL_HALLUCINATION: [], LABEL_GROUNDED_ERROR: []}
    for s in samples:
        lbl = s["oracle_label"]
        if lbl in by_label:
            by_label[lbl].append(s)

    min_size = min(len(v) for v in by_label.values() if v) or 1
    n = target_each if target_each is not None else min_size

    balanced: List[dict] = []
    for lbl, bucket in by_label.items():
        if not bucket:
            print(f"  [balance] WARNING: no samples for label {lbl}")
            continue
        chosen = rng.sample(bucket, min(n, len(bucket)))
        if len(bucket) < n:
            print(f"  [balance] {lbl}: only {len(bucket)} available, wanted {n}")
        balanced.extend(chosen)

    rng.shuffle(balanced)
    # Re-index dataset_idx after resampling
    for i, s in enumerate(balanced):
        s["dataset_idx"] = i
    return balanced


def generate(
    n_problems: int,
    model_tag: str,
    output_path: str,
    retries: int = 1,
    do_balance: bool = False,
    target_each: Optional[int] = None,
    max_each: Optional[int] = None,
    local_mbpp_path: Optional[str] = None,
) -> None:
    problems = _load_problems(n_problems, local_path=local_mbpp_path)
    if not problems:
        print("[ERROR] No problems loaded.")
        sys.exit(1)

    samples: List[dict] = []
    skipped = 0
    label_counts: dict = {LABEL_VALID: 0, LABEL_HALLUCINATION: 0, LABEL_GROUNDED_ERROR: 0}

    for prob_idx, prob in enumerate(problems):
        # Early stop: all three classes have hit max_each confirmed samples
        if max_each is not None and all(label_counts[l] >= max_each for l in label_counts):
            print(f"\n[early-stop] All classes reached {max_each} samples after "
                  f"{prob_idx} problems — stopping.")
            break

        task = prob["prompt"]
        tests_str = "\n".join(prob["tests"])
        fake_lib = _FAKE_LIBS[prob_idx % len(_FAKE_LIBS)]
        fn_name = _extract_fn_name(prob["tests"])

        variants = [
            ("direct",       _PROMPT_DIRECT.format(task=task, fn_name=fn_name),                              0.2),
            ("hallucinated", _PROMPT_HALLUCINATE.format(task=task, fake_lib=fake_lib, fn_name=fn_name),      0.0),
            ("grounded_err", _PROMPT_GROUNDED_ERROR.format(task=task, fn_name=fn_name),                      0.3),
        ]

        for strategy, prompt, temp in variants:
            target_label = _STRATEGY_TARGET[strategy]

            # Skip this strategy if we already have enough of its target label
            if max_each is not None and label_counts[target_label] >= max_each:
                continue

            best_code = best_label = best_error = best_exc = None
            hit_target = False

            for attempt in range(max(1, retries)):
                try:
                    raw = _call_ollama(prompt, model_tag, temperature=temp)
                    code = _extract_code(raw)
                    if not code:
                        continue

                    label, error_msg, exc_type = execute_code(code, tests_str, timeout=5)

                    # Always keep the first attempt as fallback
                    if best_code is None:
                        best_code, best_label = code, label
                        best_error, best_exc = error_msg, exc_type

                    if label == target_label:
                        best_code, best_label = code, label
                        best_error, best_exc = error_msg, exc_type
                        hit_target = True
                        break  # Got the label we wanted — no more retries needed

                except Exception as exc:
                    print(f"  [ERR attempt {attempt+1}] {prob['id']} / {strategy}: {exc}")

            if best_code is None:
                print(f"  [SKIP] {prob['id']} / {strategy}: no usable response after {retries} attempt(s)")
                skipped += 1
                continue

            label_counts[best_label] += 1
            target_note = "" if hit_target else f" (target={target_label}, missed)"
            samples.append({
                "id": f"{prob['id']}_{strategy}_{len(samples)}",
                "prompt_id": prob["id"],
                "source": prob["source"],
                "source_id": prob["source_id"],
                "prompt": task,
                "tests": tests_str,
                "code": best_code,
                "model": model_tag,
                "temperature": temp,
                "oracle_label": best_label,
                "generation_strategy": strategy,
                "execution_error": best_error,
                "execution_exc_type": best_exc or "",
                "dataset_idx": len(samples),
            })

            counts_str = f"V={label_counts[LABEL_VALID]} H={label_counts[LABEL_HALLUCINATION]} E={label_counts[LABEL_GROUNDED_ERROR]}"
            print(
                f"  [{prob_idx+1:3d}/{len(problems)}]"
                f"  {best_label:15s}"
                f"  {(best_exc or ''):22s}"
                f"  [{strategy:13s}]{target_note}"
                f"  {prob['id']}"
                f"  [{counts_str}]"
            )

        # Checkpoint every 5 problems
        if (prob_idx + 1) % 5 == 0:
            _write(samples, output_path)
            print(f"  [checkpoint] {len(samples)} samples -> {output_path}")

    # ---- Post-hoc balancing ----
    if do_balance:
        print(f"\n[balance] Before: {Counter(s['oracle_label'] for s in samples)}")
        samples = balance_samples(samples, target_each=target_each)
        print(f"[balance] After:  {Counter(s['oracle_label'] for s in samples)}")

    _write(samples, output_path)

    counts = Counter(s["oracle_label"] for s in samples)
    total = len(samples)
    print(f"\n{'='*60}")
    print(f"Done: {total} samples  ({skipped} skipped)")
    for lbl in (LABEL_VALID, LABEL_GROUNDED_ERROR, LABEL_HALLUCINATION):
        n = counts.get(lbl, 0)
        pct = f"{n/total*100:.1f}%" if total else "0%"
        print(f"  {lbl:17s}: {n:4d}  ({pct})")
    print(f"Output: {output_path}")


def _write(samples: list, path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(samples, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Generate execution-oracle dataset from MBPP problems"
    )
    ap.add_argument("--mbpp-path", default=None,
                    help="Path to local MBPP .jsonl file (highest priority; "
                         "gives access to all 974 problems without HuggingFace)")
    ap.add_argument("--problems", type=int, default=20,
                    help="MBPP problems to use (default: 20)")
    ap.add_argument("--model", default="qwen", choices=["qwen", "llama3"],
                    help="Ollama model for generation (default: qwen)")
    ap.add_argument("--retries", type=int, default=1,
                    help="Max regeneration attempts per strategy/problem until "
                         "oracle label matches the intended label (default: 1)")
    ap.add_argument("--balance", action="store_true",
                    help="Undersample majority classes for equal label distribution")
    ap.add_argument("--target-each", type=int, default=None,
                    help="Samples per label after balancing (default: min class size)")
    ap.add_argument("--max-each", type=int, default=None,
                    help="Stop generating once every label class has this many confirmed "
                         "samples (early stop — saves time when using large --problems)")
    ap.add_argument("--output", default=None,
                    help="Output JSON path")
    args = ap.parse_args()

    model_tag = "qwen2.5-coder:7b" if args.model == "qwen" else "llama3:latest"
    output = args.output or f"results/dataset_oracle_{args.problems}problems.json"

    print(
        f"[oracle] model={model_tag}  problems={args.problems}"
        f"  retries={args.retries}  balance={args.balance}"
        f"  max-each={args.max_each or '(none)'}  mbpp-path={args.mbpp_path or '(auto)'}"
        f"  output={output}"
    )
    t0 = time.time()
    generate(
        args.problems, model_tag, output,
        retries=args.retries,
        do_balance=args.balance,
        target_each=args.target_each,
        max_each=args.max_each,
        local_mbpp_path=args.mbpp_path,
    )
    print(f"Wall-clock: {(time.time()-t0)/60:.2f} min")


if __name__ == "__main__":
    main()

import json
from typing import List
# Let's import CodeSample by appending its path at runtime in main
# but for linting we try:
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.dataset import CodeSample


class PromptGenerator:
    """
    Parses CodeHalu-style benchmark JSON files.
    For this Prototype, it provides hardcoded mock variants of generation (A "Perfect LLM", a "Buggy Logic LLM", and a "Hallucinating LLM")
    so we can evaluate our auto-labeling pipeline without hitting paid OpenAI APIs.
    """
    
    @staticmethod
    def generate_mock_dataset(benchmark_path: str) -> List[dict]:
        """
        Reads a benchmark JSON file and generates 3 distinct responses per question.
        Returns a list of raw dicts that we will run through executor.
        """
        with open(benchmark_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        generated_samples = []
        for item in data[:5]:  # Take first 5 tasks for mock run
            qid = item["id"]
            question = item["question"]
            tests = item.get("solutions", [""])[0] if item.get("solutions") else ""
            
            # Variant 1: Valid
            generated_samples.append({
                "id": f"{qid}_Llama3_Valid",
                "prompt": question,
                "generated_code": "def solve(*args): return 0  # Just syntax valid string\nimport math\nmath.sqrt(4)",
                "tests": "assert True" # mock test
            })
            
            # Variant 2: Grounded Error (Math fail)
            generated_samples.append({
                "id": f"{qid}_GPT3_LogicFail",
                "prompt": question,
                "generated_code": "def solve(*args): return 1\nassert 1 == 2", # failing assertion represents failed logic test
                "tests": ""
            })
            
            # Variant 3: Hallucinated
            generated_samples.append({
                "id": f"{qid}_Mistral_Hallucination",
                "prompt": question,
                "generated_code": "import sys\nimport hallucinated_tensorflow as htf\nhtf.init_model()",
                "tests": ""
            })
            
        return generated_samples

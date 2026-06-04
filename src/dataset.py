from pydantic import BaseModel
from typing import List, Optional
import json

class CodeSample(BaseModel):
    """
    Standard schema for a single instance of LLM-generated code to be evaluated.
    """
    id: str
    prompt: str
    generated_code: str
    # Context describes the structural implication, useful for semantic verification
    code_context: Optional[str] = None
    expected_api_version: str = "v1"

class DatasetLoader:
    """
    Utility class for parsing lines of structured JSONL data into typed CodeSample objects.
    Ensures safe parsing of data prior to passing it to the AST code analyzer.
    """
    @staticmethod
    def load_jsonl(filepath: str) -> List[CodeSample]:
        samples = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip():
                        continue
                    data = json.loads(line)
                    samples.append(CodeSample(**data))
        except FileNotFoundError:
            print(f"Warning: Dataset file not found at {filepath}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON on line: {e}")
        return samples

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.dataset import CodeSample
from src.classifier import CodeClassifier

class PipelineEvaluator:
    """
    Feeds the auto-labeled (execution oracle) dataset into the static CodeClassifier Prototype
    and compares the precision/recall metrics.
    """
    
    def __init__(self):
        self.classifier = CodeClassifier(
            gt_version="v1",
            use_dynamic_gt=True,
            enable_cache=True
        )

    def evaluate_dataset(self, samples: list):
        """
        Takes a list of pre-executed and auto-labeled samples, formats them as CodeSample,
        and runs the prototype.
        """
        prototype_samples = []
        for s in samples:
            prototype_samples.append(CodeSample(
                id=s["id"],
                prompt=s["prompt"],
                generated_code=s["code"],
                code_context=s["oracle_label"]  # We use code_context field to hold expected label
            ))
            
        print(f"\n--- Running Automated Pipeline Evaluation on {len(prototype_samples)} Samples ---")
        correct = 0
        
        for sample in prototype_samples:
            result = self.classifier.classify(sample)
            
            # Map result back to high-level labels
            predicted_label = "VALID"
            if result.is_grounded_error:
                predicted_label = "GROUNDED_ERROR"
            elif result.hallucination_category:
                predicted_label = "HALLUCINATION"
                
            expected = sample.code_context
            match = (predicted_label == expected)
            if match: correct += 1
            
            print(f"[{'PASS' if match else 'FAIL'}] ID: {sample.id}")
            print(f"  Oracle Label:   {expected}")
            print(f"  Static Predict: {predicted_label}")
            print(f"  Explanation:    {result.explanation}")
            
        acc = correct / len(prototype_samples) * 100 if prototype_samples else 0
        print(f"\n===========================================")
        print(f"PIPELINE AUTOMATED ACCURACY: {acc:.2f}%")
        print(f"===========================================")
        return acc

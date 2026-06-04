import sys
import traceback
from typing import Tuple, Dict

class ExecutionOracle:
    """
    Executes Python code dynamically to act as the Ground Truth Oracle.
    If the code raises ModuleNotFoundError or AttributeError for unknown APIs,
    it auto-labels it as HALLUCINATION. If logic fails (Assertion), GROUNDED_ERROR.
    """
    
    @staticmethod
    def execute_and_label(code: str, tests: str = "") -> Tuple[str, str]:
        """
        Executes code safely (as safe as `exec` can be locally, for research only)
        Returns: (Label, Error_Message)
        Label can be: VALID, HALLUCINATION, GROUNDED_ERROR, SYNTAX_ERROR
        """
        sandbox_env: Dict[str, str] = {}
        full_code = code + "\n" + tests
        
        try:
            # We redirect stdout temporarily to prevent clutter
            # In a real secure pipeline, you'd use a Docker container.
            exec(full_code, sandbox_env)
            return "VALID", ""
            
        except SyntaxError as e:
            return "SYNTAX_ERROR", str(e)
            
        except (ModuleNotFoundError, ImportError) as e:
            # Fake/hallucinated modules
            return "HALLUCINATION", f"Missing Module: {str(e)}"
            
        except NameError as e:
            # Variables or functions fabricated out of thin air
            return "HALLUCINATION", f"Fabricated Name: {str(e)}"
            
        except AttributeError as e:
            # Calling fake methods on real objects
            return "HALLUCINATION", f"Fabricated Attribute: {str(e)}"
            
        except AssertionError as e:
            # Failed the unit tests but code structure was valid
            return "GROUNDED_ERROR", "Test Failed"
            
        except Exception as e:
            # Any other runtime exception is a logical grounded error
            return "GROUNDED_ERROR", f"Runtime Error: {type(e).__name__} - {str(e)}"

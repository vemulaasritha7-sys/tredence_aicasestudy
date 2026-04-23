import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from intent_analyzer import analyze_intent

class PlannerError(Exception):
    pass

def create_plan(user_input):
    """
    Consumes intent matrices returning a strict list execution array dynamically.
    """
    parsed = analyze_intent(user_input)
    
    # Always format to array constraint returning exact boundaries back downwards
    plan_block = {
        "action": parsed["action"],
        "filename": parsed["target_file"],
        "value": user_input,
        "recipient": parsed.get("metadata", {}).get("recipient", "")
    }

    return [plan_block]

plan = create_plan

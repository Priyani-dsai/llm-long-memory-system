"""
Interpreter output schema.

Defines the structured format produced by the interpreter
when analyzing a user turn.
"""

"""
Interpreter output schema.

Defines the structure of the object returned by interpret_turn().
This file contains no logic — schema only.
"""


INTERPRETER_OUTPUT_SCHEMA = {
    "intent_type": str,
    "action": {
        "name": (str, type(None)),
        "parameters": dict,
    },
    "temporal_scope": {
        "type": str,      # e.g. "global", "date", "task"
        "value": (str, type(None)),
    },
    "override_signal": {
        "explicit": bool,
        "target_key": (str, type(None)),
    },
    "memory_policy_signal": {
        "affects_memory": bool,
        "policy_type": (str, type(None)),
    },
    "confidence": float,
}

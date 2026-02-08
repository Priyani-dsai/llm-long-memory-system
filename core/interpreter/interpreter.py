"""
Interpreter module.

Responsible for converting natural language user input
into structured, machine-readable intent representations.
"""


def interpret_turn(
    user_message: str,
    recent_turns: list[dict],
    turn_id: int
) -> dict:
    """
    Returns structured interpretation of the user turn.

    Output contract (must always return valid JSON-compatible dict):

    {
        "intent_type": str,
        "action": {
            "name": str | None,
            "parameters": dict
        },
        "temporal_scope": {
            "type": str,
            "value": str | None
        },
        "override_signal": {
            "explicit": bool,
            "target_key": str | None
        },
        "memory_policy_signal": {
            "affects_memory": bool,
            "policy_type": str | None
        },
        "confidence": float
    }

    Notes:
    - This function MUST NOT return free-form text.
    - All fields must be present in the returned dict.
    - Any uncertainty should be reflected via confidence values,
      not by omitting fields.
    """
    raise NotImplementedError

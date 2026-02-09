"""
Interpreter module.

Responsible for converting natural language user input
into structured, machine-readable intent representations.
"""


"""
Minimal interpreter implementation.

This is a deterministic, rule-based interpreter
used only for end-to-end pipeline validation.
"""

from typing import Dict, List


def interpret_turn(
    user_message: str,
    recent_turns: List[Dict],
    turn_id: int
) -> Dict:
    text = user_message.lower()

    # ---- Intent detection (very coarse) ----
    if "prefer" in text:
        intent_type = "update_preference"
    elif "call" in text and ("tomorrow" in text or "at" in text):
        intent_type = "make_commitment"
    elif "call" in text:
        intent_type = "perform_action"
    else:
        intent_type = "ask_general_question"

    # ---- Action detection ----
    action_name = None
    if "call" in text:
        action_name = "call"

    # ---- Temporal scope ----
    if "tomorrow" in text:
        temporal_scope = {"type": "date", "value": "tomorrow"}
    else:
        temporal_scope = {"type": "global", "value": None}

    # ---- Override detection (not active yet) ----
    override_signal = {
        "explicit": False,
        "target_key": None,
    }

    # ---- Memory policy signal ----
    memory_policy_signal = {
        "affects_memory": intent_type in {"update_preference", "make_commitment"},
        "policy_type": None,
    }

    return {
        "intent_type": intent_type,
        "action": {
            "name": action_name,
            "parameters": {},
        },
        "temporal_scope": temporal_scope,
        "override_signal": override_signal,
        "memory_policy_signal": memory_policy_signal,
        "confidence": 0.8,
    }

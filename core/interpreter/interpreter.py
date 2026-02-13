"""
Interpreter module.

Responsible for converting natural language user input
into structured, machine-readable intent representations.
"""


import json
from typing import Dict, List
from core.llm.llm_client import call_llm
from core.interpreter.schema import INTERPRETER_OUTPUT_SCHEMA
from pathlib import Path
from typing import List, Dict

MAX_RETRIES = 2
PROMPT_PATH = Path(__file__).parent / "interpreter_prompt.txt"


def _validate_schema(obj: Dict) -> bool:
    required_keys = INTERPRETER_OUTPUT_SCHEMA.keys()
    return all(key in obj for key in required_keys)

def _build_prompt(
    user_message: str,
    recent_turns: List[Dict]
) -> str:
    """
    Builds the full interpreter prompt.
    """

    system_prompt = PROMPT_PATH.read_text().strip()

    context_lines = []
    for turn in recent_turns[-3:]:
        context_lines.append(f"User: {turn['user']}")
        context_lines.append(f"Assistant: {turn['assistant']}")

    context_block = "\n".join(context_lines)

    prompt = (
        f"{system_prompt}\n\n"
        f"Conversation context:\n"
        f"{context_block}\n\n"
        f"User input:\n"
        f"{user_message}\n\n"
        f"JSON output:\n"
    )

    return prompt

def _normalize_interpreter_output(parsed: dict) -> dict:
    # --- Ensure temporal_scope exists and is valid ---
    ts = parsed.get("temporal_scope")

    if not isinstance(ts, dict):
        parsed["temporal_scope"] = {"type": "global", "value": None}
    else:
        scope_type = ts.get("type")
        scope_value = ts.get("value", None)

        if scope_type not in {"global", "date", "task"}:
            parsed["temporal_scope"] = {"type": "global", "value": None}
        else:
            parsed["temporal_scope"] = {
                "type": scope_type,
                "value": scope_value
            }

    # --- Normalize action name ---
    if parsed.get("action", {}).get("name") in {"prefer", "like", "want"}:
        parsed["action"]["name"] = None

    # --- Correction logic ---
    if parsed.get("intent_type") == "correction":
        parsed["memory_policy_signal"] = {
            "affects_memory": False,
            "policy_type": None
        }

    # --- Ensure memory policy consistency ---
    mps = parsed.get("memory_policy_signal", {})
    if not mps.get("affects_memory", False):
        parsed["memory_policy_signal"] = {
            "affects_memory": False,
            "policy_type": None
        }

    return parsed



def interpret_turn(
    user_message: str,
    recent_turns: List[Dict],
    turn_id: int
) -> Dict:
    """
    LLM-based interpreter. Authoritative semantic parser.
    """
    
    prompt = _build_prompt(user_message, recent_turns)

    for _ in range(MAX_RETRIES):
        raw = call_llm(prompt)

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            continue

        if _validate_schema(parsed):
            parsed = _normalize_interpreter_output(parsed)
            print(">>> INTERPRETER OUTPUT:", parsed)
            return parsed

    # Hard fallback (safe default)
    return {
        "intent_type": "chitchat",
        "action": {"name": None, "parameters": {}},
        "temporal_scope": {"type": "global", "value": None},
        "override_signal": {"explicit": False, "target_key": None},
        "memory_policy_signal": {"affects_memory": False, "policy_type": None},
        "confidence": 0.3,
    }

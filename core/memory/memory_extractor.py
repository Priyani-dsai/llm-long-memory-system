"""
Memory extractor module.

Extracts atomic memory objects from user input.
"""

from typing import List, Dict
import json
from core.llm.llm_client import call_llm
from pathlib import Path
import uuid

PROMPT_PATH = Path(__file__).parent / "memory_extractor_prompt.txt"


def _build_prompt(user_message: str, interpreter_output: dict) -> str:
    """
    Builds the prompt for semantic memory extraction.
    """
    system_prompt = PROMPT_PATH.read_text().strip()

    payload = {
        "user_message": user_message,
        "interpreter_output": interpreter_output,
    }

    return (
        system_prompt
        + "\n\n"
        + "==============================\n"
        + "INPUT\n"
        + "==============================\n"
        + json.dumps(payload, indent=2)
    )


def extract_memories(
    user_message: str,
    interpreter_output: Dict,
    turn_id: int
) -> List[Dict]:

    # Guard 1: memory not allowed
    if not interpreter_output["memory_policy_signal"]["affects_memory"]:
        return []

    # Guard 2: non-durable intents
    if interpreter_output["intent_type"] in {"chitchat", "query_information"}:
        return []

    prompt = _build_prompt(user_message, interpreter_output)
    raw = call_llm(prompt)

    try:
        extracted = json.loads(raw)
    except json.JSONDecodeError:
        return []

    memories = []
    for m in extracted:
        memories.append({
            "memory_id": str(uuid.uuid4()),
            "type": m["type"],
            "domain": m["domain"],
            "scope": m["scope"],
            "priority": m["priority"],
            "confidence": m["confidence"],
            "source_type": "user",
            "origin_turn": turn_id,
            "last_used_turn": turn_id,
            "status": "active",
        })

    return memories

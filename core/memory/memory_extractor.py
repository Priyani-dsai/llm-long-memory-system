"""
Memory extractor module.

Extracts atomic memory objects from user input.
"""

from typing import List, Dict
import uuid


def extract_memories(
    user_message: str,
    interpreter_output: Dict,
    turn_id: int
) -> List[Dict]:
    """
    Extracts structured memory objects from user input.
    """

    memories: List[Dict] = []

    intent = interpreter_output.get("intent_type")

    # Only extract memory for certain intents
    if intent not in {"update_preference", "make_commitment"}:
        return memories

    action = interpreter_output.get("action", {}).get("name")

    memory = {
        "memory_id": str(uuid.uuid4()),
        "type": "preference" if intent == "update_preference" else "commitment",
        "domain": action or "general",
        "scope": interpreter_output.get("temporal_scope", {"type": "global", "value": None}),
        "priority": "medium",
        "confidence": interpreter_output.get("confidence", 0.5),
        "source_type": "user",
        "origin_turn": turn_id,
        "last_used_turn": turn_id,
        "status": "active",
    }

    memories.append(memory)
    return memories

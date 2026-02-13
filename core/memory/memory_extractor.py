"""
Memory extractor module.

Extracts atomic memory objects from interpreter output.
Deterministic version (no LLM dependency).
"""

from typing import List, Dict
import uuid


def _build_memory_object(
    *,
    memory_type: str,
    domain: str,
    scope: Dict,
    priority: str,
    confidence: float,
    turn_id: int,
) -> Dict:
    """
    Constructs a normalized memory object.
    """

    return {
        "memory_id": str(uuid.uuid4()),
        "type": memory_type,
        "domain": domain,
        "scope": scope,
        "priority": priority,
        "confidence": confidence,
        "source_type": "user",
        "origin_turn": turn_id,
        "last_used_turn": turn_id,
        "status": "active",
    }


def extract_memories(
    user_message: str,
    interpreter_output: Dict,
    turn_id: int
) -> List[Dict]:
    """
    Deterministically extract memory objects from interpreter output.
    """

    intent = interpreter_output.get("intent_type")
    action = interpreter_output.get("action", {})
    action_name = action.get("name")
    scope = interpreter_output.get("temporal_scope", {})
    affects_memory = interpreter_output.get("memory_policy_signal", {}).get("affects_memory", False)
    confidence = interpreter_output.get("confidence", 0.8)

    # Guard 1: memory not allowed
    if not affects_memory:
        return []

    # Guard 2: ignore non-durable intents
    if intent in {"chitchat", "query_information", "proposed_commitment"}:
        return []

    memories: List[Dict] = []

    # -----------------------------
    # update_preference
    # -----------------------------
    if intent == "update_preference" and action_name:
        memories.append(
            _build_memory_object(
                memory_type="preference",
                domain=f"{action_name}ing",
                scope=scope,
                priority="medium",
                confidence=max(0.7, confidence),
                turn_id=turn_id,
            )
        )

    # -----------------------------
    # make_commitment
    # -----------------------------
    elif intent == "make_commitment" and action_name:
        memories.append(
            _build_memory_object(
                memory_type="commitment",
                domain=f"{action_name}ing",
                scope=scope,
                priority="high",
                confidence=max(0.9, confidence),
                turn_id=turn_id,
            )
        )

    # -----------------------------
    # update_instruction
    # -----------------------------
    elif intent == "update_instruction" and action_name:
        memories.append(
            _build_memory_object(
                memory_type="instruction",
                domain=f"{action_name}ing",
                scope={"type": "global", "value": None},
                priority="medium",
                confidence=max(0.7, confidence),
                turn_id=turn_id,
            )
        )

    # -----------------------------
    # meta_instruction (disable memory)
    # -----------------------------
    elif intent == "meta_instruction":
        memories.append(
            _build_memory_object(
                memory_type="instruction",
                domain="memory_policy",
                scope={"type": "global", "value": None},
                priority="high",
                confidence=0.9,
                turn_id=turn_id,
            )
        )

    return memories

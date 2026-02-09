"""
Memory retrieval module.

Selects candidate memories relevant to the current turn.
"""

from typing import List, Dict

from core.memory.memory_store import fetch_memories
from core.retrieval.retrieval_rules import (
    INTENT_TO_MEMORY_TYPES,
    ACTION_TO_DOMAINS,
    CONFIDENCE_THRESHOLDS,
    MAX_MEMORIES_PER_TYPE,
)


def _is_scope_applicable(scope: Dict, interpreter_output: Dict) -> bool:
    """
    Determines whether a memory scope applies to the current turn.
    """
    scope_type = scope.get("type")

    if scope_type == "global":
        return True

    if scope_type == "date":
        return scope.get("value") == interpreter_output.get("temporal_scope", {}).get("value")

    if scope_type == "task":
        return scope.get("value") == interpreter_output.get("action", {}).get("name")

    return False


def retrieve_memories(
    interpreter_output: Dict,
    turn_id: int
) -> List[Dict]:
    """
    Returns candidate memory objects for the current turn.

    Applies:
    - intent-based type selection
    - domain filtering
    - confidence thresholds
    - scope applicability
    - per-type memory limits
    """
    intent = interpreter_output.get("intent_type")
    action_name = interpreter_output.get("action", {}).get("name")

    memory_types = INTENT_TO_MEMORY_TYPES.get(intent, [])
    domains = ACTION_TO_DOMAINS.get(action_name, [])

    if not memory_types or not domains:
        return []

    candidates = fetch_memories(
        types=memory_types,
        domains=domains,
        status="active",
    )

    # Apply confidence threshold
    filtered = [
        m for m in candidates
        if m.get("confidence", 0.0) >= CONFIDENCE_THRESHOLDS.get(m.get("type"), 0.0)
    ]

    # Apply scope filtering
    scoped = [
        m for m in filtered
        if _is_scope_applicable(m.get("scope", {}), interpreter_output)
    ]

    # Limit number of memories per type
    result: List[Dict] = []
    per_type_count = {}

    for memory in scoped:
        m_type = memory.get("type")
        per_type_count.setdefault(m_type, 0)

        if per_type_count[m_type] < MAX_MEMORIES_PER_TYPE.get(m_type, 5):
            result.append(memory)
            per_type_count[m_type] += 1

    return result

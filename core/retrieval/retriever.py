"""
Memory retrieval module.
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
    scope_type = scope.get("type")
    current_scope = interpreter_output.get("temporal_scope", {})

    if scope_type == "global":
        return True

    if scope_type == "date":
        return (
            current_scope.get("type") == "date"
            and scope.get("value") == current_scope.get("value")
        )

    if scope_type == "task":
        return (
            interpreter_output.get("action", {}).get("name")
            == scope.get("value")
        )

    return False


def retrieve_memories(
    interpreter_output: Dict,
    turn_id: int
) -> List[Dict]:

    intent = interpreter_output.get("intent_type")
    action_name = interpreter_output.get("action", {}).get("name")

    memory_types = INTENT_TO_MEMORY_TYPES.get(intent, [])

    if not memory_types:
        return []

    # Domain resolution
    if intent == "query_information":
    # For queries, do NOT restrict by domain
        domains = []
    elif action_name:
        action_name = action_name.lower().strip()
        domains = ACTION_TO_DOMAINS.get(action_name, [action_name])
    else:
        domains = ["general"]


    domain_specific = fetch_memories(
        types=memory_types,
        domains=domains,
        status="active"
    )

    general = fetch_memories(
        types=memory_types,
        domains=["general"],
        status="active"
    )

    print(">>> DOMAIN SPECIFIC FETCH:", domain_specific)
    print(">>> GENERAL FETCH:", general)

    # Deduplicate
    seen = set()
    candidates = []

    for m in domain_specific + general:
        if m["memory_id"] not in seen:
            candidates.append(m)
            seen.add(m["memory_id"])
    
    print(">>> FETCHED RAW CANDIDATES:", candidates)

    # Confidence filter
    filtered = [
        m for m in candidates
        if m.get("confidence", 0.0)
        >= CONFIDENCE_THRESHOLDS.get(m.get("type"), 0.0)
    ]

    # Scope filter
    scoped = [
        m for m in filtered
        if _is_scope_applicable(m.get("scope", {}), interpreter_output)
    ]

    # Per-type limit
    result: List[Dict] = []
    per_type_count = {}

    for memory in scoped:
        m_type = memory.get("type")
        per_type_count.setdefault(m_type, 0)

        if per_type_count[m_type] < MAX_MEMORIES_PER_TYPE.get(m_type, 5):
            result.append(memory)
            per_type_count[m_type] += 1

    return result

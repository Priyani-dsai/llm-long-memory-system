"""
Conflict resolution module.
"""

from typing import List, Dict


TYPE_PRECEDENCE = {
    "constraint": 5,
    "exception": 4,
    "commitment": 3,
    "instruction": 2,
    "preference": 1,
    "profile_fact": 0,
}

SCOPE_PRECEDENCE = {
    "task": 3,
    "date": 2,
    "global": 1,
}

PRIORITY_RANK = {
    "high": 3,
    "medium": 2,
    "low": 1,
}


def _scope_rank(memory: Dict) -> int:
    return SCOPE_PRECEDENCE.get(
        memory.get("scope", {}).get("type"),
        0
    )


def _sort_memories(memories: List[Dict]) -> List[Dict]:
    return sorted(
        memories,
        key=lambda m: (
            TYPE_PRECEDENCE.get(m.get("type"), 0),
            _scope_rank(m),
            PRIORITY_RANK.get(m.get("priority"), 0),
        ),
        reverse=True,
    )


def resolve_conflicts(
    memories: List[Dict],
    interpreter_output: Dict,
    turn_id: int
) -> List[Dict]:
    """
    Returns ordered effective memory set.
    """
    if not memories:
        return []

    ordered = _sort_memories(memories)
    return ordered

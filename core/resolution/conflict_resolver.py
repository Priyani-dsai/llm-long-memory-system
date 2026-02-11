"""
Conflict resolution module.

Resolves contradictions between retrieved memories and
determines the effective rule set for the current turn.
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


def _scope_rank(memory: Dict) -> int:
    return SCOPE_PRECEDENCE.get(
        memory.get("scope", {}).get("type"),
        0
    )


def _sort_memories(memories: List[Dict]) -> List[Dict]:
    """
    Sort memories by:
    1. Type strength
    2. Scope specificity
    3. Priority
    """
    return sorted(
        memories,
        key=lambda m: (
            TYPE_PRECEDENCE.get(m.get("type"), 0),
            _scope_rank(m),
            m.get("priority") == "high",
        ),
        reverse=True,
    )


def _apply_exceptions(
    memories: List[Dict]
) -> List[Dict]:
    """
    Applies exception memories to override their targets.
    """
    overridden_ids = set()

    for memory in memories:
        if memory.get("type") == "exception":
            target_id = memory.get("target_memory_id")
            if target_id:
                overridden_ids.add(target_id)

    return [
        m for m in memories
        if m.get("memory_id") not in overridden_ids
    ]


def _validate_commitments(
    memories: List[Dict]
) -> List[Dict]:
    """
    Removes commitments whose required constraints
    are no longer active.
    """
    active_constraints = {
        m.get("memory_id")
        for m in memories
        if m.get("type") == "constraint"
    }

    valid = []

    for memory in memories:
        if memory.get("type") == "commitment":
            required = set(memory.get("constraints_applied", []))
            if not required.issubset(active_constraints):
                continue
        valid.append(memory)

    return valid


def resolve_conflicts(
    memories: List[Dict],
    interpreter_output: Dict,
    turn_id: int
) -> List[Dict]:
    """
    Resolves conflicts and returns the effective memory rules.
    """
    if not memories:
        return []

    # Step 1: sort by strength
    ordered = _sort_memories(memories)

    # Step 2: apply exceptions
    without_overridden = _apply_exceptions(ordered)

    # Step 3: validate commitments
    validated = _validate_commitments(without_overridden)

    return validated




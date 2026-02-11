"""
Memory policy module.

Controls whether memory objects are allowed to be written
or updated based on active policy rules.
"""

from typing import Dict, List


def is_memory_write_allowed(
    memory_candidate: Dict,
    active_policies: List[Dict]
) -> bool:
    """
    Determines whether a memory object is allowed to be stored.

    Policy examples:
    - User says "don't remember this"
    - System policy disables profile storage
    """

    # If no active policies, allow by default
    if not active_policies:
        return True

    for policy in active_policies:
        policy_type = policy.get("policy_type")

        # Explicit memory disable
        if policy_type == "disable_memory":
            return False

        # Block profile facts
        if (
            policy_type == "disable_profile_memory"
            and memory_candidate.get("type") == "profile_fact"
        ):
            return False

    return True

def decide_memory_write(
    *,
    memory_candidate: Dict,
    existing_memory: Dict | None,
    current_turn: int
) -> Dict:
    """
    Decides whether to insert a new memory or update an existing one.

    Returns a dict:
    {
        "action": "insert" | "update" | "ignore",
        "memory": Dict
    }
    """

    # No existing memory → insert
    if existing_memory is None:
        return {
            "action": "insert",
            "memory": memory_candidate,
        }

    # Same turn duplicate → ignore
    if existing_memory.get("origin_turn") == current_turn:
        return {
            "action": "ignore",
            "memory": existing_memory,
        }

    # Otherwise → update existing memory
    updated = existing_memory.copy()

    # Confidence reinforcement (simple rule)
    updated["confidence"] = max(
        existing_memory.get("confidence", 0.5),
        memory_candidate.get("confidence", 0.5),
    )

    updated["last_used_turn"] = current_turn

    return {
        "action": "update",
        "memory": updated,
    }


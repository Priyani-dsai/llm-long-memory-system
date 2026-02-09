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

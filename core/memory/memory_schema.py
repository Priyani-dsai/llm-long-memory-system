"""
Memory schema definitions.

Defines the structure of all memory objects used
by the long-term memory system.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, List

# --------------------
# Memory Types
# --------------------
MEMORY_TYPE_CONSTRAINT = "constraint"
MEMORY_TYPE_PREFERENCE = "preference"
MEMORY_TYPE_INSTRUCTION = "instruction"
MEMORY_TYPE_EXCEPTION = "exception"
MEMORY_TYPE_COMMITMENT = "commitment"
MEMORY_TYPE_PROFILE = "profile_fact"

# --------------------
# Status Values
# --------------------
STATUS_ACTIVE = "active"
STATUS_INACTIVE = "inactive"
STATUS_OVERRIDDEN = "overridden"
STATUS_EXPIRED = "expired"

# --------------------
# Priority Levels
# --------------------
PRIORITY_HIGH = "high"
PRIORITY_MEDIUM = "medium"
PRIORITY_LOW = "low"


@dataclass
class BaseMemory:
    """
    Base class for all memory objects.

    This defines the canonical structure used across
    storage, retrieval, conflict resolution, and decay.
    """
    memory_id: str
    type: str
    domain: str
    scope: Dict[str, Optional[str]]
    priority: str
    confidence: float
    source_type: str
    origin_turn: int
    last_used_turn: int
    status: str = STATUS_ACTIVE

    def is_active(self) -> bool:
        return self.status == STATUS_ACTIVE

    def touch(self, current_turn: int) -> None:
        """
        Update last-used timestamp when memory is applied.
        """
        self.last_used_turn = current_turn


@dataclass
class ConstraintMemory(BaseMemory):
    """
    Hard rule that must always be enforced unless
    explicitly overridden by a valid exception.
    """
    pass


@dataclass
class PreferenceMemory(BaseMemory):
    """
    Soft preference that can be ignored if conflicting
    with higher-priority rules.
    """
    pass


@dataclass
class InstructionMemory(BaseMemory):
    """
    Persistent instruction about how the assistant
    should behave.
    """
    pass


@dataclass
class ExceptionMemory(BaseMemory):
    """
    Temporary or scoped override to an existing constraint
    or instruction.
    """
    target_memory_id: Optional[str] = None


@dataclass
class CommitmentMemory(BaseMemory):
    """
    A commitment created after resolving constraints
    and exceptions for a specific scope.
    """
    constraints_applied: List[str] = field(default_factory=list)


@dataclass
class ProfileFactMemory(BaseMemory):
    """
    Long-lived factual information about the user.
    """
    pass

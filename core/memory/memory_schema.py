"""
Memory schema definitions.

Defines the structure of all memory objects used
by the long-term memory system.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class BaseMemory:
    memory_id: str
    type: str
    domain: str
    scope: Dict
    priority: str
    confidence: float
    source_type: str
    origin_turn: int
    last_used_turn: int
    status: str


@dataclass
class ConstraintMemory(BaseMemory):
    pass


@dataclass
class PreferenceMemory(BaseMemory):
    pass


@dataclass
class InstructionMemory(BaseMemory):
    pass


@dataclass
class ExceptionMemory(BaseMemory):
    pass


@dataclass
class CommitmentMemory(BaseMemory):
    pass


@dataclass
class ProfileFactMemory(BaseMemory):
    pass

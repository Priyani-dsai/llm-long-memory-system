"""
Interpreter output schema.

Defines the structured format produced by the interpreter
when analyzing a user turn.
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ActionSchema:
    name: Optional[str]
    parameters: Dict


@dataclass
class TemporalScopeSchema:
    type: str
    value: Optional[str]


@dataclass
class OverrideSignalSchema:
    explicit: bool
    target_key: Optional[str]


@dataclass
class MemoryPolicySignalSchema:
    affects_memory: bool
    policy_type: Optional[str]


@dataclass
class InterpreterOutput:
    intent_type: str
    action: ActionSchema
    temporal_scope: TemporalScopeSchema
    override_signal: OverrideSignalSchema
    memory_policy_signal: MemoryPolicySignalSchema
    confidence: float

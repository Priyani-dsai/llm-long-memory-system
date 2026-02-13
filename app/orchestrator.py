"""
Orchestrator module.

Controls the end-to-end execution of a single
conversation turn.
"""

from typing import List, Dict

from core.memory.memory_store import (
    store_memory,
    update_memory,
    find_existing_memory,
)

from core.memory.memory_policy import (
    is_memory_write_allowed,
    decide_memory_write,
)

from core.interpreter.interpreter import interpret_turn
from core.memory.memory_extractor import extract_memories
from core.retrieval.retriever import retrieve_memories
from core.resolution.conflict_resolver import resolve_conflicts
from core.injection.injector import build_system_context
from core.llm.llm_client import generate_response
from core.memory.decay_manager import apply_decay



# Short-term context (FIFO)
_SHORT_TERM_CONTEXT: List[Dict] = []
MAX_CONTEXT_TURNS = 3


def _update_short_term_context(
    turn_id: int,
    user_message: str,
    assistant_message: str
) -> None:
    _SHORT_TERM_CONTEXT.append({
        "turn_id": turn_id,
        "user": user_message,
        "assistant": assistant_message,
    })

    if len(_SHORT_TERM_CONTEXT) > MAX_CONTEXT_TURNS:
        _SHORT_TERM_CONTEXT.pop(0)


def process_turn(
    user_message: str,
    turn_id: int
) -> str:

    # 1. Interpret
    interpreter_output = interpret_turn(
        user_message=user_message,
        recent_turns=_SHORT_TERM_CONTEXT,
        turn_id=turn_id,
    )

    # 2. Extract memory candidates
    memory_candidates = extract_memories(
        user_message=user_message,
        interpreter_output=interpreter_output,
        turn_id=turn_id,
    )

    print(">>> MEMORY CANDIDATES:", memory_candidates)

    # 3. Store / Update memories
    active_policies = []  # later this can be derived from memory_policy_signal

    for memory in memory_candidates:

        if not is_memory_write_allowed(memory, active_policies):
            continue

        existing = find_existing_memory(
            memory_type=memory["type"],
            domain=memory["domain"],
            scope=memory["scope"]
        )

        decision = decide_memory_write(
            memory_candidate=memory,
            existing_memory=existing,
            current_turn=turn_id
        )

        if decision["action"] == "insert":
            store_memory(decision["memory"])

        elif decision["action"] == "update":
            update_memory(
                memory_id=decision["memory"]["memory_id"],
                updates=decision["memory"]
            )

        # ignore → do nothing

    
     # 3.5 Apply decay (NEW STEP)
    apply_decay(current_turn=turn_id)

    print(">>> STARTING RETRIEVAL FOR:", interpreter_output)

    # 4. Retrieval
    retrieved_memories = retrieve_memories(
        interpreter_output=interpreter_output,
        turn_id=turn_id,
    )

    # 5. Conflict Resolution
    resolved_memories = resolve_conflicts(
        memories=retrieved_memories,
        interpreter_output=interpreter_output,
        turn_id=turn_id,
    )

    # 6. Update usage metadata (CRITICAL FIX)
    for memory in resolved_memories:
        update_memory(
            memory_id=memory["memory_id"],
            updates={"last_used_turn": turn_id}
        )

    print(">>> RESOLVED MEMORIES:", resolved_memories)

    # 7. Injection
    system_context = build_system_context(resolved_memories)

    # 8. Generate Response
    assistant_response = generate_response(
        system_context=system_context,
        recent_turns=_SHORT_TERM_CONTEXT,
        user_message=user_message,
    )

    # 9. Update short-term context
    _update_short_term_context(
        turn_id=turn_id,
        user_message=user_message,
        assistant_message=assistant_response,
    )

    return assistant_response

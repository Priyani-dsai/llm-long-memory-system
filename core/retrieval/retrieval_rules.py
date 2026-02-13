"""
Retrieval rules configuration.

Defines how interpreter outputs map to memory retrieval
behavior.
"""

# Intent → which memory types are relevant
INTENT_TO_MEMORY_TYPES = {

    # Immediate actions → need constraints + preferences
    "perform_action": [
        "constraint",
        "exception",
        "preference",
        "instruction",
    ],

    # Confirmed future commitment
    "make_commitment": [
        "constraint",
        "exception",
        "commitment",
    ],

    # Proposed future action → no memory influence yet
    "proposed_commitment": [],

    # Stable preference update
    "update_preference": [
        "preference",
        "constraint",
    ],

    # System behavior change
    "update_instruction": [
        "instruction",
    ],

    # Ask about schedule or stored facts
    "query_information": [
    "commitment",
    "constraint",
    "instruction",
    "preference"
    ],


    # Correction may affect factual memory
    "correction": [
        "commitment",
        "profile_fact",
    ],

    # Memory-related instruction
    "meta_instruction": [
        "instruction",
    ],

    # Social
    "chitchat": [],
}


# Action → semantic domains
ACTION_TO_DOMAINS = {
    "call": ["calling"],
    "message": ["communication"],
    "pay": ["payment"],
    "schedule": ["planning"],
    "book": ["booking"],
    "default": ["general"],
}


# Minimum confidence required per memory type
CONFIDENCE_THRESHOLDS = {
    "constraint": 0.7,
    "exception": 0.6,
    "commitment": 0.6,
    "instruction": 0.5,
    "preference": 0.4,
    "profile_fact": 0.6,
}

# Maximum number of memories retrieved per type
MAX_MEMORIES_PER_TYPE = {
    "constraint": 5,
    "exception": 3,
    "commitment": 3,
    "instruction": 5,
    "preference": 5,
    "profile_fact": 3,
}

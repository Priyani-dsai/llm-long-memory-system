"""
Retrieval rules configuration.

Defines how interpreter outputs map to memory retrieval
behavior.
"""

# Intent → which memory types are relevant
INTENT_TO_MEMORY_TYPES = {
    "perform_action": [
        "constraint",
        "exception",
        "commitment",
        "instruction",
        "preference",
    ],
    "ask_general_question": [],
    "update_preference": [
        "preference",
        "instruction",
    ],
    "make_commitment": [
        "constraint",
        "exception",
        "commitment",
    ],
}

# Action → semantic domains
ACTION_TO_DOMAINS = {
    "call": ["calling", "communication"],
    "message": ["communication"],
    "schedule": ["planning"],
    "default": [],
}

# Minimum confidence required per memory type
CONFIDENCE_THRESHOLDS = {
    "constraint": 0.7,
    "exception": 0.6,
    "commitment": 0.6,
    "instruction": 0.5,
    "preference": 0.4,
    "profile_fact": 0.8,
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

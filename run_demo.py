"""
run_demo.py

Deterministic demonstration of hybrid long-term memory pipeline.
"""

import sqlite3
import json
import os

from app.orchestrator import process_turn, reset_short_term_context
from core.memory.memory_store import DB_PATH, _initialize_db


def print_separator():
    print("\n" + "=" * 60 + "\n")


def reset_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    _initialize_db()
    reset_short_term_context()
    print("[✓] Database reset for deterministic run.")


def print_active_memories():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT memory_json FROM memories WHERE status = 'active'"
    )
    rows = cursor.fetchall()

    print("\nActive Stored Memories:")
    if not rows:
        print("- None")
    else:
        for row in rows:
            memory = json.loads(row["memory_json"])
            print(
                f"- {memory['type']} | "
                f"{memory['domain']} | "
                f"scope={memory['scope']} | "
                f"confidence={memory['confidence']:.2f}"
            )

    conn.close()


def run_demo():
    reset_database()

    turn = 1

    print_separator()
    print("Turn 1: Storing global preference")
    response = process_turn("I prefer calls after 11 AM.", turn)
    print("Assistant:", response)
    turn += 1

    print_separator()
    print("Turn 2: Attempt conflicting commitment")
    response = process_turn("Schedule a call at 9 AM tomorrow.", turn)
    print("Assistant:", response)
    turn += 1

    print_separator()
    print("Turn 3: Valid commitment")
    response = process_turn("Schedule a call at 2 PM tomorrow.", turn)
    print("Assistant:", response)
    turn += 1

    print_separator()
    print("Turn 4–10: Noise conversation")
    for _ in range(6):
        process_turn("Nice weather today.", turn)
        turn += 1

    print_separator()
    print("Turn 11: Long-range recall")
    response = process_turn("What calls are scheduled tomorrow?", turn)
    print("Assistant:", response)

    print_separator()
    print_active_memories()
    print_separator()
    print("Demo completed successfully.")


if __name__ == "__main__":
    run_demo()

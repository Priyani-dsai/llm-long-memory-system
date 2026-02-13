"""
run_demo.py

Deterministic demonstration of long-term memory pipeline.
"""

import sqlite3
import json
from app.orchestrator import process_turn


def print_separator():
    print("\n" + "=" * 60 + "\n")


def print_active_memories():
    conn = sqlite3.connect("storage/symbolic_memory.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT memory_json FROM memories WHERE status = 'active'")
    rows = cursor.fetchall()

    print("Active Stored Memories:")
    for row in rows:
        memory = json.loads(row["memory_json"])
        print(f"- {memory['type']} | {memory['domain']} | scope={memory['scope']}")

    conn.close()


def run_demo():
    turn = 1

    print_separator()
    print("Turn 1: Storing global preference")
    print("User: I prefer calls after 11 AM.")
    response = process_turn("I prefer calls after 11 AM.", turn)
    print("Assistant:", response)
    turn += 1

    print_separator()
    print("Turn 2: Attempt conflicting commitment")
    print("User: Schedule a call at 9 AM tomorrow.")
    response = process_turn("Schedule a call at 9 AM tomorrow.", turn)
    print("Assistant:", response)
    turn += 1

    print_separator()
    print("Turn 3: Valid commitment")
    print("User: Schedule a call at 2 PM tomorrow.")
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
    print("User: What calls are scheduled tomorrow?")
    response = process_turn("What calls are scheduled tomorrow?", turn)
    print("Assistant:", response)

    print_separator()
    print_active_memories()
    print_separator()
    print("Demo complete.")


if __name__ == "__main__":
    run_demo()

"""
Evaluation script for Long-Term Memory System.

Runs controlled benchmark conversations and reports:
- Retrieval correctness
- Long-range recall
- Conflict handling
- Decay behavior
- Latency
"""

import os
import time
import sqlite3

from app.main import process_turn  # adjust if needed
from core.memory.memory_store import fetch_memories
from core.memory.decay_manager import apply_decay
from core.memory.memory_store import _initialize_db


DB_PATH = "storage/symbolic_memory.db"


# -------------------------
# Utility
# -------------------------

def reset_db():
    import os
    from core.memory.memory_store import DB_PATH, _initialize_db

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    _initialize_db()
    print("[✓] Database reset.")



def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# -------------------------
# Benchmark 1
# Global Preference Recall
# -------------------------

def benchmark_preference_conflict():
    print_section("Benchmark 1 — Global Preference Conflict")

    turn = 1
    process_turn("I prefer calls after 11 AM.", turn)
    turn += 1

    start = time.time()
    response = process_turn("Schedule a call at 9 AM tomorrow.", turn)
    latency = time.time() - start

    print("\nAssistant Response:")
    print(response)
    print("\nLatency:", round(latency, 3), "sec")


# -------------------------
# Benchmark 2
# Date Commitment Recall
# -------------------------

def benchmark_commitment_recall():
    print_section("Benchmark 2 — Date Commitment Recall")

    turn = 1
    process_turn("Call mom tomorrow.", turn)
    turn += 1

    # simulate filler turns (no memory writes)
    for i in range(2, 8):
        process_turn("Okay.", i)

    response = process_turn("What do I have tomorrow?", 8)

    print("\nAssistant Response:")
    print(response)


# -------------------------
# Benchmark 3
# Retrieval Precision
# -------------------------

def benchmark_retrieval_precision():
    print_section("Benchmark 3 — Retrieval Precision")

    turn = 1
    process_turn("I prefer calling.", turn)
    turn += 1

    process_turn("I like Italian food.", turn)
    turn += 1

    response = process_turn("Schedule a call.", turn)

    print("\nAssistant Response:")
    print(response)

    memories = fetch_memories(types=[], domains=[], status="active")

    print("\nActive Memories:")
    for m in memories:
        print("-", m["type"], "|", m["domain"])


# -------------------------
# Benchmark 4
# Decay Simulation
# -------------------------

def benchmark_decay():
    print_section("Benchmark 4 — Decay Simulation")

    turn = 1
    process_turn("Call mom tomorrow.", turn)

    print("\nBefore Decay:")
    memories = fetch_memories(types=[], domains=[], status="active")
    for m in memories:
        print("Confidence:", m["confidence"])

    # simulate long gap
    apply_decay(current_turn=100)

    print("\nAfter Decay to Turn 100:")
    memories = fetch_memories(types=[], domains=[], status="active")
    for m in memories:
        print("Confidence:", m["confidence"])


# -------------------------
# Benchmark 5
# Latency Measurement
# -------------------------

def benchmark_latency():
    print_section("Benchmark 5 — Latency")

    turn = 1
    latencies = []

    for i in range(1, 6):
        start = time.time()
        process_turn("Call mom tomorrow.", i)
        latencies.append(time.time() - start)

    avg = sum(latencies) / len(latencies)

    print("Per-turn latencies:", [round(l, 3) for l in latencies])
    print("Average latency:", round(avg, 3), "sec")


# -------------------------
# Main
# -------------------------

if __name__ == "__main__":
    reset_db()

    benchmark_preference_conflict()
    reset_db()

    benchmark_commitment_recall()
    reset_db()

    benchmark_retrieval_precision()
    reset_db()

    benchmark_decay()
    reset_db()

    benchmark_latency()

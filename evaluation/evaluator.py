"""
Evaluation script for Hybrid Long-Term Memory System.

Benchmarks:
- Global preference conflict handling
- Date-based commitment recall
- Retrieval precision
- Memory decay
- Latency measurement
"""

import os
import time

from app.orchestrator import process_turn, reset_short_term_context
from core.memory.memory_store import (
    fetch_memories,
    _initialize_db,
    DB_PATH
)
from core.memory.decay_manager import apply_decay


# -------------------------------------------------
# Utility
# -------------------------------------------------

def reset_db():
    """
    Ensures deterministic benchmark execution.
    Resets DB and short-term context.
    """
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    _initialize_db()
    reset_short_term_context()

    print("[✓] Database + context reset.")


def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# -------------------------------------------------
# Benchmark 1 — Preference Conflict
# -------------------------------------------------

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


# -------------------------------------------------
# Benchmark 2 — Long-Range Commitment Recall
# -------------------------------------------------

def benchmark_commitment_recall():
    print_section("Benchmark 2 — Date Commitment Recall")

    turn = 1
    process_turn("Call mom tomorrow.", turn)
    turn += 1

    # Insert noise turns
    for i in range(2, 8):
        process_turn("Nice weather today.", i)

    response = process_turn("What do I have tomorrow?", 8)

    print("\nAssistant Response:")
    print(response)


# -------------------------------------------------
# Benchmark 3 — Retrieval Precision
# -------------------------------------------------

def benchmark_retrieval_precision():
    print_section("Benchmark 3 — Retrieval Precision")

    turn = 1
    process_turn("I prefer calls after 11 AM.", turn)
    turn += 1

    process_turn("I like Italian food.", turn)  # unrelated preference
    turn += 1

    response = process_turn("Schedule a call.", turn)

    print("\nAssistant Response:")
    print(response)

    memories = fetch_memories(types=[], domains=[], status="active")

    print("\nActive Memories:")
    for m in memories:
        print("-", m["type"], "|", m["domain"])


# -------------------------------------------------
# Benchmark 4 — Decay Simulation
# -------------------------------------------------

def benchmark_decay():
    print_section("Benchmark 4 — Memory Decay Simulation")

    turn = 1
    process_turn("Call mom tomorrow.", turn)

    print("\nBefore Decay:")
    memories = fetch_memories(types=[], domains=[], status="active")
    for m in memories:
        print("Confidence:", round(m["confidence"], 3))

    apply_decay(current_turn=100)

    print("\nAfter Decay to Turn 100:")
    memories = fetch_memories(types=[], domains=[], status="active")
    for m in memories:
        print("Confidence:", round(m["confidence"], 3))


# -------------------------------------------------
# Benchmark 5 — Latency
# -------------------------------------------------

def benchmark_latency():
    print_section("Benchmark 5 — Latency")

    latencies = []

    for i in range(1, 6):
        start = time.time()
        process_turn("Call mom tomorrow.", i)
        latencies.append(time.time() - start)

    avg = sum(latencies) / len(latencies)

    print("Per-turn latencies:", [round(l, 3) for l in latencies])
    print("Average latency:", round(avg, 3), "sec")


# -------------------------------------------------
# Main
# -------------------------------------------------

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

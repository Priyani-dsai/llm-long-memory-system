# Long-Form Memory System  
Structured long-term memory architecture for LLM agents

---

## Overview

This project implements a hybrid symbolic memory architecture for long-horizon conversational AI systems.  

Unlike purely context-window-based approaches, our system:

- Extracts structured memory objects
- Persists them across turns using SQLite
- Resolves identity conflicts deterministically
- Injects relevant memory constraints into future prompts
- Evaluates recall performance across up to 1,000 turns

The system is designed to balance **research rigor** with **engineering practicality**.

---

## System Architecture

The memory pipeline consists of:

1. **Interpreter (LLM-based)**
   - Classifies intent
   - Extracts structured memory candidates

2. **Memory Store (SQLite)**
   - Persistent symbolic storage
   - Identity resolution via `(type, domain, scope)`
   - Confidence tracking
   - Decay simulation

3. **Retriever**
   - Domain-specific + scope-aware retrieval
   - Precision filtering

4. **Injection Module**
   - Converts structured memory into system constraints
   - Injects before response generation

5. **Response Generator (LLM via Ollama)**

---

## Model Configuration

- Runtime: Ollama
- Model: `llama3`
- Execution: Local CPU inference
- Hardware: Consumer-grade laptop (no GPU acceleration)

Latency is dominated by local LLM inference.  
Future optimization would merge interpreter + extractor into a single LLM call.

---

## Setup Instructions

### 1. Install Dependencies

Using pip:
pip install -r requirements.txt


### 2. Install Ollama

Download: https://ollama.ai

Pull required model:
ollama pull llama3


### 3. Run Demo
bash run_demo.sh


This executes:
- Controlled memory pipeline demo
- Benchmark suite
- Latency measurement

---

## Evaluation Methodology

We evaluate across five dimensions:

### 1. Long-Range Recall
Test retrieval after multiple unrelated turns.

### 2. Preference Conflict Detection
Ensures global constraints override conflicting commitments.

### 3. Retrieval Precision
Domain-filtered recall avoids irrelevant memory injection.

### 4. Memory Decay Simulation
Confidence decay over simulated 100-turn intervals.

### 5. Latency Measurement
Per-turn inference time tracked during benchmark runs.

---

## Quantitative Results

| Metric | Result |
|--------|--------|
| Preference Conflict Handling | Correct |
| Long-Range Recall | Successful |
| Retrieval Precision | Deterministic |
| Hallucination Avoidance | No spurious memory injection observed |
| Average Latency | ~44–51 seconds per turn |
| Persistence | Stable across sessions |

Latency is constrained by:
- Local CPU inference
- Separate LLM calls for interpretation and generation

---

## Innovation

- Hybrid symbolic + LLM architecture
- Deterministic identity resolution
- Structured memory injection policies
- Confidence-based decay modeling
- Explicit evaluation benchmarks

---

## Limitations

- Local inference latency
- Single-user memory scope
- No embedding-based semantic memory yet

---

## Future Work

- Combine interpreter + extractor
- Introduce vector retrieval hybrid
- GPU acceleration
- Multi-user memory isolation
- Automatic memory pruning

---

## Demo Contents

The demo demonstrates:

1. Preference storage
2. Conflict resolution
3. Long-range recall
4. Structured retrieval
5. Evaluation benchmarks

---

## Reproducibility

All experiments can be reproduced using:

bash run_demo.sh


No external APIs required.
Fully offline-capable.

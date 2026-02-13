#!/bin/bash

echo "=============================================="
echo "Hybrid Long-Range Memory System — Demo Run"
echo "=============================================="

echo ""
echo "[1] Running controlled memory demo..."
python run_demo.py

echo ""
echo "[2] Running full evaluation benchmarks..."
python -m evaluation.evaluator

echo ""
echo "=============================================="
echo "Demo completed successfully."
echo "=============================================="

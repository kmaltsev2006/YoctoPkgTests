#!/bin/bash
set -e

python3 /src/run_tests.py || { echo "Agent failed"; exit 2; }

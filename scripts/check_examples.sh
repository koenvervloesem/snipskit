#!/bin/bash
set -e

cd examples

# Extract the example from README.rst
tail -n +$(grep -n 'code-block:: python' ../README.rst | cut -d: -f1) ../README.rst > README.example
# The following line needs GNU head. Use tail -r | tail -n +3 | tail -r instead of head -n -2 on BSD systems.
head -n $(grep -n 'end-code-block' README.example | cut -d: -f1) README.example | tail -n +3 | head -n -2 | sed 's/^    //' > README.py

# Check the examples in the examples directory.
pylint -E *.py

# Clean up the files from the extracted code.
rm README.example README.py

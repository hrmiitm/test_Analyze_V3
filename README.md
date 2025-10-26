# Analyze_V3

This repository contains:

- execute.py — a small data analysis script that reads `data.csv` and prints JSON to stdout.
- data.csv — source data converted from the provided `data.xlsx`.
- .github/workflows/ci.yml — CI workflow that runs ruff, executes the script, and publishes `result.json` to GitHub Pages.

CI behavior

- On push, the workflow will install Python 3.11, install dependencies (including pandas 2.3), run `ruff .` (the linter), execute `python execute.py > result.json`, and publish the produced `result.json` via GitHub Pages.

Notes

- Do NOT commit `result.json` — it should be produced by CI and published by the workflow.
- To run locally, install the dependencies (`pip install pandas==2.3.0`) and run `python execute.py`.

#!/usr/bin/env python3
"""
Data Analysis Script
Reads data.csv and performs revenue analysis

This version fixes a naming/robustness issue and ensures compatibility with
Python 3.11+ and pandas 2.3.
"""

from pathlib import Path
import pandas as pd
import json
import sys


def main():
    csv_path = Path(__file__).parent / "data.csv"
    if not csv_path.exists():
        print(f"Error: data file not found at {csv_path}", file=sys.stderr)
        sys.exit(2)

    try:
        df = pd.read_csv(csv_path)
    except Exception as exc:
        print(f"Error reading CSV: {exc}", file=sys.stderr)
        sys.exit(3)

    # Ensure Revenue column exists and is numeric
    if "Revenue" not in df.columns:
        print("Error: required column 'Revenue' not found in data", file=sys.stderr)
        sys.exit(4)

    # Coerce to numeric to avoid issues with formatting
    df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce")

    # Compute metrics
    total_revenue = df["Revenue"].sum(skipna=True)

    # Guard against empty groups / all-NaN revenue
    if df["Revenue"].dropna().empty:
        region_revenue = {}
        product_revenue = {}
        top_region = None
    else:
        region_revenue = df.groupby("Region")["Revenue"].mean().to_dict()
        product_revenue = df.groupby("Product")["Revenue"].mean().to_dict()
        # idxmax on the sum per region; if tie, idxmax returns one of them
        try:
            top_region = df.groupby("Region")["Revenue"].sum().idxmax()
        except Exception:
            top_region = None

    results = {
        "total_revenue": float(total_revenue) if pd.notna(total_revenue) else None,
        "avg_revenue_by_region": {k: float(v) for k, v in region_revenue.items()},
        "avg_revenue_by_product": {k: float(v) for k, v in product_revenue.items()},
        "top_region": top_region,
        "total_records": int(len(df)),
    }

    # Print to stdout as JSON so CI can capture it with `> result.json`
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

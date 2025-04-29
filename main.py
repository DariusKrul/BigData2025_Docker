#!/usr/bin/env python3
"""
CLI: Generate descriptive statistics for a CSV dataset.
Outputs summary.csv (always) and summary.parquet (if pyarrow is available).
"""
import argparse
from pathlib import Path
import pandas as pd


def summarize(input_path: str, output_dir: str = "output") -> None:
    """Read CSV → write summary stats as CSV (+ Parquet if pyarrow present)."""
    df = pd.read_csv(input_path)
    summary = df.describe(include="all")

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = out_dir / "summary.csv"
    summary.to_csv(csv_path)

    # Optional Parquet output
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq

        table = pa.Table.from_pandas(summary)
        pq.write_table(table, out_dir / "summary.parquet")
    except ImportError:
        pass

    try:
        rel_path = csv_path.relative_to(Path.cwd())
    except ValueError:
        rel_path = csv_path
    print(f"✅  Summary written to {rel_path}")


def cli() -> None:
    parser = argparse.ArgumentParser(
        description="Generate summary statistics for a CSV and save them as CSV (and Parquet).",
    )
    parser.add_argument("input", help="Path to input CSV file")
    parser.add_argument(
        "-o", "--output", default="output", help="Output directory (default: ./output)"
    )
    args = parser.parse_args()
    summarize(args.input, args.output)


if __name__ == "__main__":
    cli()
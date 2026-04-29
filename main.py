#!/usr/bin/env python3
"""
CLI: Generate descriptive statistics for a CSV dataset.

Outputs (all written to --output directory):
  summary.csv         – describe() for all columns
  summary.parquet     – same, in Parquet format (requires pyarrow)
  missing.csv         – missing-value count & percentage per column
  correlations.csv    – Pearson correlation matrix (numeric columns only)
  dtypes.csv          – column names, dtype, and nullable flag
"""
import argparse
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------------------------
# Core analysis helpers
# ---------------------------------------------------------------------------

def _describe(df: pd.DataFrame) -> pd.DataFrame:
    """Standard descriptive statistics for all columns."""
    return df.describe(include="all")


def _missing(df: pd.DataFrame) -> pd.DataFrame:
    """Count and percentage of missing values per column."""
    counts = df.isnull().sum()
    pct = (counts / len(df) * 100).round(2)
    return pd.DataFrame({"missing_count": counts, "missing_pct": pct})


def _correlations(df: pd.DataFrame) -> pd.DataFrame | None:
    """Pearson correlation matrix for numeric columns. Returns None if < 2 numeric cols."""
    numeric = df.select_dtypes(include="number")
    if numeric.shape[1] < 2:
        return None
    return numeric.corr(method="pearson")


def _dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Column name, dtype, and whether the column contains any nulls."""
    return pd.DataFrame(
        {
            "dtype": df.dtypes.astype(str),
            "has_nulls": df.isnull().any(),
            "unique_values": df.nunique(),
        }
    )


# ---------------------------------------------------------------------------
# Main summarise routine
# ---------------------------------------------------------------------------

def summarize(input_path: str, output_dir: str = "output") -> None:
    """Read *input_path* CSV and write all summary artefacts to *output_dir*."""
    df = pd.read_csv(input_path)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    written: list[str] = []

    # 1. Descriptive statistics (always)
    summary = _describe(df)
    csv_path = out_dir / "summary.csv"
    summary.to_csv(csv_path)
    written.append(str(csv_path))

    # 1b. Parquet version (optional – needs pyarrow)
    try:
        import pyarrow as pa          # noqa: F401
        import pyarrow.parquet as pq  # noqa: F401

        pq.write_table(pa.Table.from_pandas(summary), out_dir / "summary.parquet")
        written.append(str(out_dir / "summary.parquet"))
    except ImportError:
        pass

    # 2. Missing-value report (always)
    missing_path = out_dir / "missing.csv"
    _missing(df).to_csv(missing_path)
    written.append(str(missing_path))

    # 3. Correlation matrix (numeric columns only)
    corr = _correlations(df)
    if corr is not None:
        corr_path = out_dir / "correlations.csv"
        corr.to_csv(corr_path)
        written.append(str(corr_path))
    else:
        print("ℹ️  Skipping correlations.csv – fewer than 2 numeric columns found.")

    # 4. Data-type summary (always)
    dtypes_path = out_dir / "dtypes.csv"
    _dtypes(df).to_csv(dtypes_path)
    written.append(str(dtypes_path))

    # --- summary printout ---
    print(f"\n📊  Input : {input_path}  ({len(df):,} rows × {len(df.columns)} cols)")
    print(f"📁  Output: {out_dir}/")
    for path in written:
        try:
            rel = Path(path).relative_to(Path.cwd())
        except ValueError:
            rel = Path(path)
        print(f"   ✅  {rel}")


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

def cli() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate summary statistics for a CSV and save them as CSV (and Parquet). "
            "Also produces missing-value report, correlation matrix, and dtype summary."
        ),
    )
    parser.add_argument("input", help="Path to input CSV file")
    parser.add_argument(
        "-o", "--output", default="output", help="Output directory (default: ./output)"
    )
    args = parser.parse_args()
    summarize(args.input, args.output)


if __name__ == "__main__":
    cli()

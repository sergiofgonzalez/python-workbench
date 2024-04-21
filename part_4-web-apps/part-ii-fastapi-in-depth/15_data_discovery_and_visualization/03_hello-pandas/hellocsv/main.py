"""Entry point for the application."""

import sys

import pandas as pd


def from_csv_get_df(filename: str) -> pd.DataFrame:
    """Read a CSV file and return a pandas DataFrame."""
    return pd.read_csv(filename, sep="|")


if __name__ == "__main__":
    data = from_csv_get_df(sys.argv[1])
    print(data.head(5))

"""Illustrate how to work with nested list comprehensions."""

def main() -> None:
    """Application entry point."""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    years = range(2020, 2026)
    months_with_years = [
        [f"{month}, {year}"
         for month in months]
        for year in years
    ]
    print(f"Months with years: {months_with_years}")

    print("=" * 80)
    for i, vector in enumerate(months_with_years):
        print(f"Vector[{i}]: {vector}")


if __name__ == "__main__":
    main()

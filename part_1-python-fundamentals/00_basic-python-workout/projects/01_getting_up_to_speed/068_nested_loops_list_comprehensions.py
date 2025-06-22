"""Illustrate how to use nested loops in list comprehensions."""

def main() -> None:
    """Application entry point."""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    years = range(2020, 2026)
    months_with_years = [f"{month}, {year}"
                         for year in years
                         for month in months]
    print(f"Months with years: {months_with_years}")


if __name__ == "__main__":
    main()

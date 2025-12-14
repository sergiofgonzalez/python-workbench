"""Compute basic statistics on data retrieved from a file."""

from pathlib import Path

file_path = Path("data/temp_readings_heathrow.txt")


def main() -> None:
    """Application entry point."""
    with file_path.open("r", encoding="utf-8") as file:
        lines = file.readlines()
        readings = [float(line.strip()) for line in lines if line.strip()]

    if not readings:
        print("No data available.")
        return

    total = sum(readings)
    count = len(readings)
    average = total / count
    minimum = min(readings)
    maximum = max(readings)
    median = (
        sorted(readings)[count // 2]
        if count % 2 == 1
        else (sorted(readings)[count // 2 - 1] + sorted(readings)[count // 2]) / 2
    )

    print(f"Total Readings: {count}")
    print(f"Lowest Reading: {minimum:.2f}")
    print(f"Highest Reading: {maximum:.2f}")
    print(f"Average Reading: {average:.2f}")
    print(f"Median Reading: {median:.2f}")
    print(f"Number of unique Readings: {len(set(readings))}")


if __name__ == "__main__":
    main()

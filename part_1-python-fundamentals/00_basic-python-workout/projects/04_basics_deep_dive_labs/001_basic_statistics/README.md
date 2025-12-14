# 001: basic statistics
> reading temperature readings from a file and printing some basic statistics

Given a file with the monthly high temperature at Heathrow airport from 1948 to 2017 (data/in_data/380_basic_statistics/temp_heathrow.txt), read the file and find the following basic statistics without relying on any module:

1. Highest and lowest temperatures
1. Mean temperature (i.e., the average temperature)
1. Median temperature
1. Calculate the number of unique temperatures found in the file

### Solution

1. You start by creating a directory to host your project. Because it's a simple program, you can just create a directory and copy a simple `pyproject.toml` well configured from another project. (NOTE: using `uv init` in this type of workspace will update an upstream `pyproject.toml` and complicate things unnecessarily).

The ideal `pyproject.toml` should look like the following:

    ```toml
    [project]
    name = "001-basic-statistics"
    version = "0.1.0"
    description = "Lab 001: Basic Statistics"
    readme = "README.md"
    requires-python = ">=3.12"
    dependencies = []

    [dependency-groups]
    dev = [
      "ruff>=0.14.8",
    ]

    [tool.ruff]

    ignore = [
      "T201", # Allow print statements
    ]

    # Enable all rules
    select = ["ALL"]

    [tool.ruff.lint.pydocstyle]
    convention = "google"
    ```

  Note that it just features ruff because the project is simple enough and doesn't require tests.

1. Then, you just need to type the solution in `main.py`. The following sections will feature the annotated solution.

1. You start by importing `Path` as that's the recommended way to interact with files and paths in modern Python. Because it is a simple program, you can define a global `file_path` pointing to the file with the temperature readings:

    ```python
    from pathlib import Path

    file_path = Path("data/temp_readings_heathrow.txt")
    ```

1. Then you should start by opening the file for reading, placing all the information retrieved from the file in a list:

    ```python
    with file_path.open("r", encoding="utf-8") as file:
        lines = file.readlines()
        readings = [float(line.strip()) for line in lines if line.strip()]
    ```

    You might be tempted not to use `readlines()` and go line-by-line to prevent materializing the whole list in memory (we don't know how large the file could be). However, because we need to compute the median, which is the value at the middle once the temperature readings have been sorted, it makes sense to read the file at once.

1. Then you can add a simple guardrail if nothing was read from the file, otherwise, you do the calculation:

    ```python
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
    ```

    Note that median is implemented as the value in the middle if the list has an even number of elements, or the average between the elements at the middle otherwise. This is not important.

1. Finally, you just create a basic report making sure that floating-point numbers are displayed with two decimal digits:

    ```python
    print(f"Total Readings: {count}")
    print(f"Lowest Reading: {minimum:.2f}")
    print(f"Highest Reading: {maximum:.2f}")
    print(f"Average Reading: {average:.2f}")
    print(f"Median Reading: {median:.2f}")
    print(f"Number of unique Readings: {len(set(readings))}")
    ```


## Running the program

You can run the application with:

```bash
uv run main.py
```


"""Illustrate how to use slice objects to make sense of complicated data."""

data = """
0....5..............20..........................48......
1001 Laundry        Wash all clothes            3
1002 Museum Visit   Go to the Egypt exhibit     4
1003 Do Homework    Physics and math            5
1004 Go to Gym      Work out for 1 hour         2
"""


def main() -> None:
    """Application entry point."""
    lines = (
        data.strip().splitlines()
    )  # get rid of leading/trailing whitespace and split into lines
    print(lines)
    data_lines_slice = slice(1, None)  # all lines except the first
    id_field_slice = slice(0, 5)  # characters 0 to 4
    task_field_slice = slice(5, 20)  # characters 5 to 29
    desc_field_slice = slice(20, 48)  # characters 20 to 47
    priority_field_slice = slice(48, None)  # characters 48 to end

    tasks = []
    for line in lines[data_lines_slice]:
        task_id = line[id_field_slice].strip()
        task_name = line[task_field_slice].strip()
        task_desc = line[desc_field_slice].strip()
        task_priority = int(line[priority_field_slice].strip())
        tasks.append((task_id, task_name, task_desc, task_priority))

    print("Parsed Tasks:")
    for task in tasks:
        print(task)


if __name__ == "__main__":
    main()

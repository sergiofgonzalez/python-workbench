"""Illustrates how to pickle and unpickle data."""

import pickle
from pathlib import Path

file_path = Path("data/out_data/tmp/data.pkl")


def main() -> None:
    """Application entry point."""
    str_msg = "Hello to Jason!"
    task_tuple = (1001, "Homework", 5)
    task_dict = {"task_id": "1002", "title": "Laundry", "urgency": 3}
    int_num = 55
    float_num = 123.45

    with file_path.open("wb") as file:
        pickle.dump(str_msg, file)
        pickle.dump(task_tuple, file)
        pickle.dump(task_dict, file)
        pickle.dump(int_num, file)
        pickle.dump(float_num, file)

    with file_path.open("rb") as file:
        unpickled_str_msg = pickle.load(file)  # noqa: S301
        unpickled_task_tuple = pickle.load(file)  # noqa: S301
        unpickled_task_dict = pickle.load(file)  # noqa: S301
        unpickled_int_num = pickle.load(file)  # noqa: S301
        unpickled_float_num = pickle.load(file)  # noqa: S301

    print(f"{unpickled_str_msg=!r}")
    print(f"{unpickled_task_tuple=!r}")
    print(f"{unpickled_task_dict=!r}")
    print(f"{unpickled_int_num=!r}")
    print(f"{unpickled_float_num=!r}")


if __name__ == "__main__":
    main()

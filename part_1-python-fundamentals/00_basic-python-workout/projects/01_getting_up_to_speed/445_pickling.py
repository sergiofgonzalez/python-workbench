"""Illustrates the basics of the pickle module."""

import math
import pickle
from pathlib import Path

base_path = Path("data", "out_data", "tmp")


def main() -> None:
    """Application entry point."""
    int_num = 42
    float_num = math.pi
    string_data = "goodbye"

    out_file = base_path / "pickled_data.pkl"
    with out_file.open("wb") as bin_file:
        int_num = 42
        float_num = math.pi
        string_data = "goodbye"
        pickle.dump(int_num, bin_file)
        pickle.dump(float_num, bin_file)
        pickle.dump(string_data, bin_file)

        int_num_2 = 55
        float_num_2 = math.e
        string_data_2 = "hello"
        pickle.dump(int_num_2, bin_file)
        pickle.dump(float_num_2, bin_file)
        pickle.dump(string_data_2, bin_file)

    print(f"Wrote pickled data to {out_file}")

    # Now let's read back the pickled data
    with out_file.open("rb") as bin_file:
        loaded_int_1 = pickle.load(bin_file)  # noqa: S301
        loaded_float_1 = pickle.load(bin_file)  # noqa: S301
        loaded_string_1 = pickle.load(bin_file)  # noqa: S301
        loaded_int_2 = pickle.load(bin_file)  # noqa: S301
        loaded_float_2 = pickle.load(bin_file)  # noqa: S301
        loaded_string_2 = pickle.load(bin_file)  # noqa: S301
    print("Unpacked pickled data:")
    print(f" 1: {loaded_int_1!r}, {loaded_float_1!r}, {loaded_string_1!r}")
    print(f" 2: {loaded_int_2!r}, {loaded_float_2!r}, {loaded_string_2!r}")


if __name__ == "__main__":
    main()

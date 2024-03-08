"""
Illustrates how to get some db load perf data using Faker
"""

from time import perf_counter

from faker import Faker
from fastapi.testclient import TestClient

from cryptid.data import explorer as data
from cryptid.data.errors import DuplicateError
from cryptid.main import app
from cryptid.model.explorer import Explorer


def load():
    f = Faker()
    num_rows = 100_000
    rows_skipped = 0
    start = perf_counter()
    for _ in range(num_rows):
        try:
            data.create(
                Explorer(
                    name=f.name(),
                    country=f.country(),
                    description=f.text(),
                )
            )
        except DuplicateError:
            rows_skipped += 1
    end = perf_counter()
    print(
        f"Loaded {num_rows - rows_skipped} records in {end - start:.2f} seconds"
    )


def read_db():
    start = perf_counter()
    _ = data.get_all()
    end = perf_counter()
    print(f"Read all records in {end - start:.2f} seconds")


def read_api():
    client = TestClient(app)
    start = perf_counter()
    _ = client.get("/explorer")
    end = perf_counter()
    print(f"Read all records via API in {end - start:.2f} seconds")


if __name__ == "__main__":
    load()
    read_db()
    read_api()

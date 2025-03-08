"""Testing the capabilities of KenobiDB."""

from kenobi import KenobiDB


def main() -> None:
    """Application entry point."""
    # Initialize the database. If the file doesn't exist it will be created.
    # SQLite is used as the storage backend. All the necessary tables and indices
    # will be created.
    db = KenobiDB("example.db")

    # Purge: removes all docs from the database
    db.purge()

    # Insert / Insert Many
    db.insert({"name": "Grogu", "color": "Green"})
    db.insert_many(
        [{"name": "Mando", "color": "Silver"}, {"name": "Vader", "color": "black"}],
    )

    # Remove
    db.remove("name", "Grogu")
    db.remove("color", "Silver")

    # Update
    db.update("name", "Vader", {"color": "Dark Black"})

    # Search Ops

    ## all: retrieve all docs with optional pagination
    records = db.all(limit=10, offset=0)
    print(records)

    records = db.all()  # no paginations
    print(records)

    ## search: Retrieve documents matching a specific key-value pair
    records = db.search("color", "Dark Black")
    print(records)

    records = db.search("name", "Vader")
    print(records)

    records = db.search("name", "Luke")
    print(records)

    ## search_pattern: retrieves documents using regex
    ## (requires a higher version than the one published)
    # records = db.search("color", "* [Bb]lack")  # noqa: ERA001
    # print(records)  # noqa: ERA001

    ## find_any: retrieve documents where a a key matches any value in a list
    records = db.find_any("color", ["Dark Black", "Shiny White"])
    print(records)

    ## find_all: retrieve document where a key matches all values in a list
    records = db.find_all("color", ["Dark Black", "Shiny White"])
    print(records)


if __name__ == "__main__":
    main()

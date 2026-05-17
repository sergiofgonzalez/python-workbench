"""Illustrates the basics of FalkorDB."""

from falkordb import FalkorDB


def main() -> None:
    """Application entry point."""
    # Connec to FalkorDB on localhost, port 6379
    db = FalkorDB("localhost", port=6379)

    # Create the 'Formula1' graph
    g = db.select_graph("Formula1")

    # Clear out the existing graph, if it exists
    g.delete()

    # Create some nodes and relationships
    g.query("""CREATE
        (:Driver {name: "Max Verstappen"})-[:drives_for]->(:Team {name: "Red Bull Racing"}),
        (:Driver {name: "Fernando Alonso"})-[:drives_for]->(:Team {name: "Aston Martin"}),
        (:Driver {name: "Lewis Hamilton"})-[:drives_for]->(:Team {name: "Ferrari"})""")  # noqa: E501

    # Query the graph to find the driver that represent Ferrari
    result = g.query("""MATCH (d:Driver)-[:drives_for]->(t:Team)
        WHERE t.name = "Ferrari"
        RETURN d.name""")

    # Print the result
    for record in result.result_set:
        print(f"Driver: {record[0]}")

    # Query how many drivers represent Red Bull Racing
    result = g.query(
        """MATCH (d:Driver)-[:drives_for]->(t:Team {name: "Red Bull Racing"}) RETURN count(d)""",  # noqa: E501
    )

    print(
        f"Number of drivers representing Red Bull Racing: {result.result_set[0][0]}",
    )


if __name__ == "__main__":
    main()

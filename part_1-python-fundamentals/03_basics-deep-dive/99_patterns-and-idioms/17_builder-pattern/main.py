"""Illustrates how to consume the BoatBuilder class to create a Boat instance."""

from boat_builder import BoatBuilder


def main() -> None:
    """Application entry point."""
    my_boat = (
        BoatBuilder()
        .with_motors(2, "Best Motor Co.", "OM123")
        .with_sails(1, "fabric", "white")
        .with_cabin()
        .with_hull_color("blue")
        .build()
    )
    my_boat.sail()


if __name__ == "__main__":
    main()

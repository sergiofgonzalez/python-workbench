"""Illustrate how to use class methods as alternative initializers."""

from collections.abc import Iterator, Sequence


class Vector3D:
    """A simple 3D vector class."""

    def __init__(self, x: float, y: float, z: float) -> None:
        """Initialize the Vector3D instance."""
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_sequence(cls, seq: Sequence[float]) -> "Vector3D":
        """Create a Vector3D instance from a sequence of three floats."""
        if len(seq) != 3:  # noqa: PLR2004
            msg = "Sequence must have exactly three elements."
            raise ValueError(msg)
        return cls(seq[0], seq[1], seq[2])

    def __repr__(self) -> str:
        """Return the string representation of the Vector3D instance."""
        return f"Vector3D(x={self.x}, y={self.y}, z={self.z})"

    def __iter__(self) -> Iterator[float]:
        """Make Vector3D instances iterable."""
        # ugly implementation
        # yield self.x
        # yield self.y
        # yield self.z
        # Pythonic implementation using yield from
        yield from (self.x, self.y, self.z)



def main() -> None:
    """Application entry point."""
    v1 = Vector3D(1.1, 2.2, 3.3)
    print(f"{v1=}")

    v2 = Vector3D.from_sequence([4.4, 5.5, 6.6])
    print(f"{v2=}")

    v3 = Vector3D.from_sequence((7.7, 8.8, 9.9))
    print(f"{v3=}")

    for coord in v3:
        print(coord)


if __name__ == "__main__":
    main()

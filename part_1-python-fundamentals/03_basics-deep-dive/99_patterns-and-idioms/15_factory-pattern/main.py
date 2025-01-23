"""Illustrates the consumer code when using the Factory pattern."""

from image import create_image


def main() -> None:
    """Application entry point."""
    image = create_image("beach.jpeg")
    print(f"{type(image)=}")

    image = create_image("diagram.png")
    print(f"{type(image)=}")

    image = create_image("meme.gif")
    print(f"{type(image)=}")

    try:
        image = create_image("banner.webp")
    except Exception as e:  # noqa: BLE001
        print(f"Error: {e} ({type(e)})")

if __name__ == "__main__":
    main()

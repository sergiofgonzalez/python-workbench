"""Lab one liner description."""

from html_generator.utils import body, html, p, text


def main() -> None:
    """Application entry point."""
    paragraph = p("This is some text wrapped in a paragraph.")
    print(paragraph)
    print("=" * 40)
    body_content = text("This is the body content.")
    body_element = body([body_content, paragraph])
    print(body_element)
    print("=" * 40)
    doc = html([body_element])
    print(doc)


if __name__ == "__main__":
    main()

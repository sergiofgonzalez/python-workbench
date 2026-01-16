"""HTML Generator Utility Classes and Functions."""

from typing import override


class HTMLElement:
    """Base class for HTML elements."""

    def __init__(self, tag: str | None, children: list["HTMLElement"]) -> None:
        """Initialize with the tag name and content."""
        self.tag = tag
        self.children = children

    def __str__(self) -> str:
        """Convert the element to an HTML string."""
        children_str = "".join(str(child) for child in self.children)
        return f"<{self.tag}>{children_str}</{self.tag}>"


class InnerText(HTMLElement):
    """Class representing inner text in HTML."""

    def __init__(self, text: str) -> None:
        """Initialize with the text content."""
        super().__init__("", [])
        self.text = text

    @override
    def __str__(self) -> str:
        """Convert the inner text to a string."""
        return self.text


class HTMLParagraph(HTMLElement):
    """Class representing an HTML paragraph."""

    def __init__(self, children: list[HTMLElement]) -> None:
        """Initialize with the paragraph text."""
        super().__init__("p", children)


class HTMLBody(HTMLElement):
    """Class representing an HTML body."""

    def __init__(self, children: list[HTMLElement]) -> None:
        """Initialize with the body content."""
        super().__init__("body", children)


class HTMLDocument(HTMLElement):
    """Class representing an entire HTML document."""

    def __init__(self, children: list[HTMLElement]) -> None:
        """Initialize with the head and body content."""
        super().__init__("html", children)


# Factory function to create HTML elements as described in the problem statement
def text(text: str) -> InnerText:
    """Create inner text for HTML elements."""
    return InnerText(text)


def p(text: str) -> HTMLParagraph:
    """Create an HTML paragraph element."""
    return HTMLParagraph([InnerText(text)])


def body(children: list[HTMLElement]) -> HTMLBody:
    """Create an HTML body element."""
    return HTMLBody(children)


def html(children: list[HTMLElement]) -> HTMLDocument:
    """Create an entire HTML document."""
    return HTMLDocument(children)

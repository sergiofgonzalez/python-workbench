# HTML Generator
> a hierarchy of classes that generate simple HTML

## Solution

To comply with what is explained in the problem statement you can prepare a naive implementation such as the following.

```python
class HTMLElement:
    """Base class for HTML elements."""

    def __init__(self, tag: str, content: str) -> None:
        """Initialize with the tag name and content."""
        self.tag = tag
        self.content = content

    def __str__(self) -> str:
        """Convert the element to an HTML string."""
        return f"<{self.tag}>{self.content}</{self.tag}>"


class HTMLParagraph(HTMLElement):
    """Class representing an HTML paragraph."""

    def __init__(self, text: str) -> None:
        """Initialize with the paragraph text."""
        super().__init__("p", text)
        self.text = text

class HTMLBody(HTMLElement):
    """Class representing an HTML body."""

    def __init__(self, content: str, subelement: HTMLElement) -> None:
        """Initialize with the body content."""
        super().__init__("body", content)
        self.subelement = subelement

    def __str__(self) -> str:
        """Convert the body to an HTML string."""
        return f"<{self.tag}>{self.content}{self.subelement}</{self.tag}>"


class HTMLDocument(HTMLElement):
    """Class representing an entire HTML document."""

    def __init__(self, subelement: HTMLBody) -> None:
        """Initialize with the head and body content."""
        super().__init__("html", "")
        self.subelement = subelement

    def __str__(self) -> str:
        """Convert the document to an HTML string."""
        return f"<html>{self.subelement}</html>"


# Factory function to create HTML elements as described in the problem statement
def p(text: str) -> HTMLParagraph:
    """Create an HTML paragraph element."""
    return HTMLParagraph(text)


def body(content: str, subelement: HTMLElement) -> HTMLBody:
    """Create an HTML body element."""
    return HTMLBody(content, subelement)


def html(subelement: HTMLBody) -> HTMLDocument:
    """Create an entire HTML document."""
    return HTMLDocument(subelement)

```

That really fits the bill as can be tested with the following `main()`:

```python
def main() -> None:
    """Application entry point."""
    paragraph = p("This is some text wrapped in a paragraph.")
    print(paragraph)
    print("=" * 40)
    body_element = body("This is the body content.", paragraph)
    print(body_element)
    print("=" * 40)
    doc = html(body_element)
    print(doc)
```

But the naive implementation cannot be taken beyond that.

A more comprehensive implementation of the HTML class hierarchy can support that use case and many other scenarios:

```python
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
```

You start by defining the `HTMLElement` class. This is the base class for all the other HTML elements and is initialized with a tag (e.g., `"p"`) and a list of children elements (e.g., a body and a paragraph element for the example given).

You can include an implementation of the `str()` function. This implementation will not work for all the elements, but that's not a problem as you'll be able to override the implementation in the concrete classes.

You have such an example for the `InnerText` implementation. This is defined to model the text you might find without additional markup as in `<body>this is some inner text...`.

The initializer requires just the text, and invokes the superclass initializer with an empty tag and list of subelements.

Additionally, because the string function needs to behave differently from the base class `__str__()`, we define a new implementation for the function and annotate it with `@override`.

The other subclasses (`HTMLParagraph`, `HTMLBody`, `HTMLDocument`, ...) don't require such customizations and can simply rely on the base class details and only define an initializer method to customize the corresponding tag.

The `main()` is slightly changed, as we need to send a list with the children elements in most of the cases.

## Running the program

See [README.md](../README.md#016-python-classes-to-generate-html) for full details.

Examples about how to run it.

You can run the application with:

```bash
uv run html-generator
```

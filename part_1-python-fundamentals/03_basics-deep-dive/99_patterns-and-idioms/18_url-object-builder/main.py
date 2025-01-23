"""Using the builder pattern to instantiate a URL object."""

from url import URL
from url_builder import URLBuilder


def main() -> None:
    """Application entry point."""
    # Building a URL object in the wild is ugly as hell
    site = URL("https", None, None, "www.example.com", None, None, None, None)
    print(site)

    # But it's a breze using the Builder
    site = URLBuilder().set_protocol("https").set_hostname("www.example.com").build()
    print(site)

    # A complete site spec
    site = (
        URLBuilder()
        .set_protocol("https")
        .set_authentication("username", "pass")
        .set_hostname("localhost", 8080)
        .set_pathname("/apis/products")
        .set_search("available=true&limit=10")
        .set_hash("ref=twitter")
        .build()
    )
    print(site)


if __name__ == "__main__":
    main()

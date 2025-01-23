"""Sending requests with the RequestBuilder."""

from request_builder import HttpMethod, RequestBuilder


def main() -> None:
    """Application entry point."""
    response = (
        RequestBuilder()
        .set_method(HttpMethod.GET)
        .set_url("http://localhost:8080/getty")
        .add_query_param("param1", "param1-value")
        .add_query_param("param1", "param1-value")
        .invoke()
    )
    print(f"{response.status_code=}")
    print(f"{response.headers}")
    print(f"{response.text}")
    print("=" * 78)

    response = (
        RequestBuilder()
        .set_method(HttpMethod.PUT)
        .set_url("http://localhost:8080/putty")
        .add_query_param("param1", "param1-value")
        .add_query_param("param1", "param1-value")
        .set_body("This is the text")
        .add_header("Content-Length", "10")
        .invoke()
    )
    print(f"{response.status_code=}")
    print(f"{response.headers}")
    print(f"{response.text}")
    print("=" * 78)

if __name__ == "__main__":
    main()

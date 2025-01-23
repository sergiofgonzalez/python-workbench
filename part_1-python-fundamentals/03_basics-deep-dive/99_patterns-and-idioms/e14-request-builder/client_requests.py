"""Illustrates how to use the requests module to send HTTP requests to the basic server."""

import requests


def main() -> None:
    """Application entry point."""
    # sending GET
    params = {
        "param1": "param1-value",
        "param2": "param2-value",
    }
    response = requests.get("http://localhost:8080/getty", params=params, timeout=30)
    print(f"{response.status_code=}")
    print(f"{response.headers}")
    print(f"{response.text}")
    print("=" * 78)

    # sending POST
    response = requests.put(
        "http://localhost:8080/putty",
        params=params,
        data="This is some text",
        timeout=30,
    )
    print(f"{response.status_code=}")
    print(f"{response.headers}")
    print(f"{response.text}")
    print("=" * 78)


if __name__ == "__main__":
    main()

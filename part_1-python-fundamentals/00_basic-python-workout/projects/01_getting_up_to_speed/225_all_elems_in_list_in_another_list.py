"""Illustrate how to check that all items in a list are in another list using sets."""


def main() -> None:
    """Application entry point."""
    good_stocks = ["AAPL", "GOOG", "AMZN", "NVDA"]
    client0_stocks = ["GOOG", "AMZN"]
    client1_stocks = ["AAPL", "SNAP"]

    all_client0_stocks_good = set(good_stocks).issuperset(client0_stocks)
    print(f"Are all client 0 stocks good? {all_client0_stocks_good}")
    all_client1_stocks_good = set(good_stocks).issuperset(client1_stocks)
    print(f"Are all client 1 stocks good? {all_client1_stocks_good}")


if __name__ == "__main__":
    main()

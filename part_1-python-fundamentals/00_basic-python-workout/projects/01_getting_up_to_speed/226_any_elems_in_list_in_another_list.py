"""Illustrate how to check that any items in a list are in another list using sets."""


def main() -> None:
    """Application entry point."""
    good_stocks = ["AAPL", "GOOG", "AMZN", "NVDA"]
    client0_stocks = ["GOOG", "AMZN"]
    client1_stocks = ["AAPL", "SNAP"]
    client2_stocks = ["TSLA", "META"]

    any_client0_stocks_good = bool(set(good_stocks).intersection(client0_stocks))
    print(f"Are any client 0 stocks good? {any_client0_stocks_good}")
    any_client1_stocks_good = bool(set(good_stocks).intersection(client1_stocks))
    print(f"Are any client 1 stocks good? {any_client1_stocks_good}")
    any_client2_stocks_good = bool(set(good_stocks).intersection(client2_stocks))
    print(f"Are any client 2 stocks good? {any_client2_stocks_good}")

    # Alternative using intersection operator &
    print("--- Alternative using & operator ---")
    any_client0_stocks_good = bool(set(good_stocks) & set(client0_stocks))
    print(f"Are any client 0 stocks good? {any_client0_stocks_good}")
    any_client1_stocks_good = bool(set(good_stocks) & set(client1_stocks))
    print(f"Are any client 1 stocks good? {any_client1_stocks_good}")
    any_client2_stocks_good = bool(set(good_stocks) & set(client2_stocks))
    print(f"Are any client 2 stocks good? {any_client2_stocks_good}")


if __name__ == "__main__":
    main()

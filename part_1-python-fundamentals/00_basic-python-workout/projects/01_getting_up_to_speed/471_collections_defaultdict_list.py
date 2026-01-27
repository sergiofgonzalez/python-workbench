"""TODO: description of the program."""
from collections import defaultdict

purchases_list = [
    (1234, 100.23),
    (345, 10.45),
    (1234, 75.00),
    (345, 222.66),
    (678, 300.25),
    (1234, 35.67),
]


def main() -> None:
    """Application entry point."""
    # Using a regular dict to group purchases by account number
    purchases_by_acct = {}
    for acct_num, amt in purchases_list:
        if acct_num in purchases_by_acct:
            purchases_by_acct[acct_num].append(amt)
        else:
            purchases_by_acct[acct_num] = [amt]
    print(purchases_by_acct)
    print("-" * 40)

    # Using defaultdict to group purchases by account number
    purchases_by_acct_dd = defaultdict(list)
    for acct_num, amt in purchases_list:
        purchases_by_acct_dd[acct_num].append(amt)
    print(purchases_by_acct_dd)
    print("-" * 40)


if __name__ == "__main__":
    main()

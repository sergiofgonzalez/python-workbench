"""Illustrate the use of the star expression when unpacking."""

from statistics import mean


def main() -> None:
    """Application entry point."""
    scores = [6.1, 6.5, 6.8, 7.1, 7.3, 7.6, 8.2, 8.9]
    min_score, *middle_scores, max_score = scores
    print(f"Minimum score: {min_score}")
    print(f"Middle scores: {middle_scores}")
    print(f"Maximum score: {max_score}")
    assert min_score == 6.1  # noqa: PLR2004
    assert middle_scores == [6.5, 6.8, 7.1, 7.3, 7.6, 8.2]
    assert max_score == 8.9  # noqa: PLR2004

    average_score = sum(scores) / len(scores)
    print(f"Average score: {average_score:.2f}")
    assert average_score == mean(scores)


if __name__ == "__main__":
    main()

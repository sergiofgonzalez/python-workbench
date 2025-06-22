"""Illustrate how to use lambdas to get more Pythonic solutions to problems."""


def main() -> None:
    """Application entry point."""
    nums = [-4, 3, 7, 0, -6]

    # Using a lambda to sort the list by absolute value
    nums.sort(key=lambda x: abs(x))
    print(f"Sorted by absolute value: {nums}")
    assert nums == [0, 3, -4, -6, 7], "The list should be sorted by absolute value"

    # scores represents tuples of Math, Science, and Art scores
    scores = [(93, 95, 94), (92, 95, 96), (94, 97, 91), (95, 97, 99)]

    # Finding the tuple with the highest score
    max_score = 0
    student_index = -1
    subject_index = -1

    for i, student in enumerate(scores):
        for j, subject_score in enumerate(student):
            if subject_score > max_score:
                max_score = subject_score
                student_index = i
                subject_index = j
    print(
        f"Max score: {max_score} "
        f"at student {student_index}, "
        f"subject {subject_index} "
        f"{scores[student_index]}",
    )

    # Using a lambda to find the tuple with the highest score
    max_score_tuple = max(
        scores,
        key=lambda student: max(student),
    )
    max_score_index = scores.index(max_score_tuple)
    max_subject_index = max_score_tuple.index(max(max_score_tuple))
    print(
        f"Max score using lambda: {max(max_score_tuple)} "
        f"at student {max_score_index}, "
        f"subject {max_subject_index} "
        f"{scores[max_score_index]}",
    )
    print("=" * 50)

    # Let's assume the highest score is the sum of the scores
    # Non-Pythonic way
    for i, student in enumerate(scores):
        score = sum(student)
        print(f"Student {i} has a total score of {score}")

    # A bit more Pythonic way
    max_score = max(sum(student) for student in scores)
    print(f"Max score (non-Pythonic): {max_score}")
    print(f"Student with max score: {scores.index(max_score_tuple)}")

    # Using a lambda to get the max score
    max_score_lambda = max(
        scores,
        key=lambda student: sum(student),
    )
    print(
        f"Max score using lambda: {sum(max_score_lambda)} "
        f"at student {scores.index(max_score_lambda)} "
        f"{max_score_lambda}",
    )


if __name__ == "__main__":
    main()

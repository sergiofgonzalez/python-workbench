"""Illustrate the concept of partial functions in Python."""

from functools import partial


def run_stats_model(dataset: str, model: str, output_path: str) -> str:
    """Run a statistical model on a dataset and save the results."""
    print(f"Running {model} on {dataset}...")
    # Simulate running the model
    result = f"Results of {model} on {dataset}"
    print(f"Saving results to {output_path}...")
    return result


# Poor man's partial function
def run_linear_regression(dataset: str) -> str:
    """Run linear regression on a dataset."""
    return run_stats_model(
        dataset,
        "linear_regression",
        "results/linear_regression_results.txt",
    )


# Partial function using functools
run_logistic_regression = partial(
    run_stats_model,
    model="logistic_regression",
    output_path="results/logistic_regression_results.txt",
)


def main() -> None:
    """Application entry point."""
    # Sample invocations: really verbose
    result = run_stats_model(
        "data.csv",
        "linear_regression",
        "results/linear_regression_results.txt",
    )
    print(f"{result}\n")

    result = run_stats_model(
        "data.csv",
        "logistic_regression",
        "results/logistic_regression_results.txt",
    )
    print(f"{result}\n")

    # Invoking poor man's partial function
    print(f"{run_linear_regression('data.csv')}\n")

    # Invoking functools.partial solution
    print(f"{run_logistic_regression('data.csv')}\n")


if __name__ == "__main__":
    main()

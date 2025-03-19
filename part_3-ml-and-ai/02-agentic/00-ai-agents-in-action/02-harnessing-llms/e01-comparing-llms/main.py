"""Main program illustrating how to use clear instructions."""

from pathlib import Path

from llm_utils import prompt_llm
import time

def list_prompt_files() -> list[Path]:
    """List all prompt files in the prompts/ directory."""
    prompts_dir = Path("prompts")
    return [
        file
        for file in prompts_dir.iterdir()
        if file.is_file() and file.suffix == ".jsonl"
    ]


def pretty_print_prompt(messages: list[dict[str, str]]) -> None:
    """Pretty print the messages in a prompt."""
    print("=" * 80)
    for message in messages:
        print(f"{message['role']}: {message['content']}")
    print()


def main() -> None:
    """Application entry point."""
    title = input("Enter a movie title: ")

    messages = [
        {
            "role": "system",
            "content": """"
                You are a famous film critic known for your rants on bad movies.",
                You will be passed a movie title delimited by XML tags and you must "
                provide a review of the movie consisting of at least 100 words "
                structured in two paragraphs.
                """,
        },
        {
            "role": "user",
            "content": f"The film to review is <MOVIE_TITLE>{title}</MOVIE_TITLE>.",
        },
    ]

    responses = {}
    print("Getting result for o3-mini: ", end="")
    start = time.perf_counter()
    response1 = prompt_llm(
        messages,
        model="o3-mini",
        deployment="o3-mini",  # only required for Azure OpenAI
    )
    print(f"{time.perf_counter() - start:.2f}s")
    responses["o3-mini"] = response1

    print("Getting result for o1: ", end="")
    start = time.perf_counter()
    response2 = prompt_llm(
        messages,
        model="o1",
        deployment="o1",  # only required for Azure OpenAI
    )
    print(f"{time.perf_counter() - start:.2f}s")
    responses["o1"] = response2

    print("Getting result for gpt4: ", end="")
    start = time.perf_counter()
    response3 = prompt_llm(
        messages,
        model="gpt4",
        deployment="chatgpt4-turbo",  # only required for Azure OpenAI
    )
    print(f"{time.perf_counter() - start:.2f}s")
    responses["gpt4"] = response3

    for model, response in responses.items():
        print(f"Model: {model}")
        print(response)
        print()

if __name__ == "__main__":
    main()

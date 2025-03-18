"""Main program illustrating how to use clear instructions."""

import json
from pathlib import Path

from llm_utils import prompt_llm


def list_prompt_files() -> list[Path]:
    """List all prompt files in the prompts/ directory."""
    prompts_dir = Path("prompts")
    return [
        file
        for file in prompts_dir.iterdir()
        if file.is_file() and file.suffix == ".jsonl"
    ]


def load_messages_from_file(file: Path) -> list[dict[str, str]]:
    """Load messages from a JSONL file."""
    result_list = []
    message_lines = ""
    with file.open() as f:
        line = f.readline()
        while line:
            line = line.strip()
            message_lines += line
            if line.strip() == "]":
                try:
                    messages = json.loads(message_lines)
                    result_list.append(messages)
                    message_lines = ""
                except json.JSONDecodeError as e:
                    print(
                        f"Error decoding messages. Please review {message_lines}: {e}",
                    )
                    raise SystemExit(1) from e
            line = f.readline()
    return result_list


def pretty_print_prompt(messages: list[dict[str, str]]) -> None:
    """Pretty print the messages in a prompt."""
    print("=" * 80)
    for message in messages:
        print(f"{message['role']}: {message['content']}")
    print()


def prompt_user_option(files: list[Path]) -> int:
    """Show the available prompt files."""
    print("Available prompt files:")
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file.name}")
    print("0. Exit")
    choice = int(input("Choose a prompt file to use: "))
    print(f"Selected: {files[choice - 1].name}")
    return choice


def main() -> None:
    """Application entry point."""
    prompt_files = list_prompt_files()
    while (choice := prompt_user_option(prompt_files)) != 0:
        for messages in load_messages_from_file(prompt_files[choice - 1]):
            pretty_print_prompt(messages)
            response = prompt_llm(
                messages,
                model="o3-mini",
                deployment="o3-mini",  # only required for Azure OpenAI
            )
            print("Response:")
            print(response)
            print("-" * 80)


if __name__ == "__main__":
    main()

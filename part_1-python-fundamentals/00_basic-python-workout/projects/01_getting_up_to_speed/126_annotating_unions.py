"""Illustrate how to annotate unions."""

from pathlib import Path
from typing import Union


def load_model(model_name: str, cache_folder: Path | str | None) -> str:
    """Load a model from the specified path or cache folder."""
    if cache_folder is None:
        return f"Loading {model_name} from default path"
    if isinstance(cache_folder, str):
        return f"Loading {model_name} from cache folder: {cache_folder}"
    return f"Loading {model_name} from cache folder path: {cache_folder.resolve()}"


def load_model_legacy_annotations(
    model_name: str,
    cache_folder: Union[Path, str, None],  # noqa: UP007
) -> str:
    """Load a model from the specified path or cache folder."""
    if cache_folder is None:
        return f"Loading {model_name} from default path"
    if isinstance(cache_folder, str):
        return f"Loading {model_name} from cache folder: {cache_folder}"
    return f"Loading {model_name} from cache folder path: {cache_folder.resolve()}"


def main() -> None:
    """Application entry point."""
    model_name = "example_model"
    cache_folder_str = "/path/to/cache"
    cache_folder_path = Path("/path/to/cache")

    print(load_model(model_name, None))
    print(load_model(model_name, cache_folder_str))
    print(load_model(model_name, cache_folder_path))


if __name__ == "__main__":
    main()

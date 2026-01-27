"""Illustrates how to create dict that allows both English and US spellings for keys."""

from collections import UserDict


class EnglishSpelledDict(UserDict):
    """A dict subclass that allows both English and US spellings for certain keys."""

    _ENG_TO_US_SPELLINGS = {  # noqa: RUF012
        "colour": "color",
        "flavour": "flavor",
        "honour": "honor",
        "neighbour": "neighbor",
        "behaviour": "behavior",
    }

    def _get_key(self, key: str) -> str:
        """Convert English spelling to US spelling if applicable."""
        if key in self._ENG_TO_US_SPELLINGS:
            return self._ENG_TO_US_SPELLINGS[key]
        return self._ENG_TO_US_SPELLINGS.get(key, key)

    def __setitem__(self, key: object, value: object) -> None:  # ty:ignore[invalid-method-override]
        """Set item, converting English spellings to US spellings."""
        if not isinstance(key, str):
            msg = "Keys must be strings"
            raise TypeError(msg)
        us_key = self._get_key(key)
        super().__setitem__(us_key, value)

    def __getitem__(self, key: object) -> object:
        """Get item, allowing both English and US spellings."""
        if not isinstance(key, str):
            msg = "Keys must be strings"
            raise TypeError(msg)
        us_key = self._get_key(key)
        return super().__getitem__(us_key)

    def get(self, key: object, default: object = None) -> object:
        """Get item using allowing both English and US spellings."""
        if not isinstance(key, str):
            msg = "Keys must be strings"
            raise TypeError(msg)
        us_key = self._get_key(key)
        return super().get(us_key, default)


def main() -> None:
    """Application entry point."""
    # create the dict using both US and English spellings
    likes = EnglishSpelledDict({"color": "blue", "flavour": "vanilla"})

    # confirm that internally it uses US spellings
    assert likes == {"color": "blue", "flavor": "vanilla"}
    print(likes)  # {'color': 'blue', 'flavor': 'vanilla'}
    print("-" * 40)

    # accesing existing keys using English spelling
    assert likes["flavour"] == "vanilla"
    print(likes["flavour"])  # vanilla
    print("-" * 40)

    # accessing existing keys using US spelling
    assert likes["flavor"] == "vanilla"
    print(likes["flavor"])
    print("-" * 40)

    # Setting a new key using English spelling
    likes["behaviour"] = "polite"
    assert likes == {
        "color": "blue",
        "flavor": "vanilla",
        "behavior": "polite",
    }
    print(likes["behavior"])
    print("-" * 40)

    # using get() method with both spellings
    print(likes.get("colour"))  # blue
    print(likes.get("color"))  # blue
    assert likes.get("colour") == "blue"
    assert likes.get("color") == "blue"
    print("-" * 40)

    # using update() method with English spelling
    likes.update({"behaviour": "gentle"})
    print(likes["behavior"])  # gentle
    assert likes == {
        "color": "blue",
        "flavor": "vanilla",
        "behavior": "gentle",
    }
    print("-" * 40)

    # adding a key that is neither English nor US spelling
    likes["size"] = "large"
    print(likes["size"])  # large
    assert likes["size"] == "large"
    print("-" * 40)


if __name__ == "__main__":
    main()

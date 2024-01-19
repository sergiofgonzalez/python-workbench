"""
Demo lib to be installed in editable mode
"""


def say_hello(name: str = None) -> None:
    print(f"Hello stranger!" if name is None else f"Hell to {name}")


def get_greeting(name: str = None) -> str:
    return f"Hello stranger!" if name is None else f"Hello to {name}"

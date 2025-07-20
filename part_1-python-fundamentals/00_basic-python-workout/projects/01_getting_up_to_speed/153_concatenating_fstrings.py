"""Illustrate how to concatenate f-strings."""


def main() -> None:
    """Application entry point."""
    settings = {
        "font_size": "large",
        "font": "Arial",
        "color": "Black",
        "align": "center",
    }
    print(f"Current settings: {settings}")
    s = ", ".join(f"{k}={v}" for k, v in settings.items())
    print(f"Concatenated settings: {s}")

    # The idea of the exercise was to illustrate the syntax for long concatenated
    # f-strings.
    long_string = (
        f"font_size={settings['font_size']}, "
        f"font={settings['font']}, "
        f"color={settings['color']}, "
        f"align={settings['align']}"
    )
    print(f"Concatenated settings: {long_string}")

    # There is an alternative syntax for long f-strings without using parentheses.
    # This is not recommended as it can lead to less readable code.
    # However, it is still valid Python syntax.
    long_string_alt = f"font_size={settings['font_size']}, " \
                      f"font={settings['font']}, " \
                      f"color={settings['color']}, " \
                      f"align={settings['align']}"  # noqa: ISC002
    print(f"Concatenated settings: {long_string_alt}")

if __name__ == "__main__":
    main()

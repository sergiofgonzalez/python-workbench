"""Image class hierarchy and factory pattern implementation."""

import re
from abc import ABC, abstractmethod
from pathlib import Path


class Image(ABC):
    """Image base class."""

    @abstractmethod
    def __init__(self, name: str) -> None:
        """Initialize abstract image instance."""
        self.name = name

    def __repr__(self) -> str:
        """Developer-level representation of the instance."""
        return "Developer level representation of the instance"

    def __str__(self) -> str:
        """User-friendly string representation of the instance."""
        return "User-friendly string representation of the instance"


class ImageJPEG(Image):
    """Class that represents a JPEG image."""

    def __init__(self, name: str) -> None:
        """Initialize an ImageJPEG instance."""
        super().__init__(name)

    def __repr__(self) -> str:
        """Developer-level representation of the instance."""
        return f"{self.__class__.__name__}({self.name})"

    def __str__(self) -> str:
        """User-friendly string representation of the instance."""
        return f"JPEG image for file {self.name}"


class ImageGIF(Image):
    """Class that represents a GIF image."""

    def __init__(self, name: str) -> None:
        """Initialize an ImageGIF instance."""
        super().__init__(name)

    def __repr__(self) -> str:
        """Developer-level representation of the instance."""
        return f"{self.__class__.__name__}({self.name})"

    def __str__(self) -> str:
        """User-friendly string representation of the instance."""
        return f"GIF image for file {self.name}"


class ImagePNG(Image):
    """Class that represents a PNG image."""

    def __init__(self, name: str) -> None:
        """Initialize an ImagePNG instance."""
        super().__init__(name)

    def __repr__(self) -> str:
        """Developer-level representation of the instance."""
        return f"{self.__class__.__name__}({self.name})"

    def __str__(self) -> str:
        """User-friendly string representation of the instance."""
        return f"PNG image for file {self.name}"


class UnsupportedImageFormatError(Exception):
    """Raised when you try to work with an unsupported image format."""


def create_image(name: str) -> Image:
    """Create an Image instance using the Factory pattern."""
    ext = Path(name).suffix
    if re.match(pattern=r".jpe?g", string=ext):
        return ImageJPEG(name)
    elif re.match(pattern=r".gif", string=ext):
        return ImageGIF(name)
    elif re.match(pattern=r".png", string=ext):
        return ImagePNG(name)
    else:
        msg = f"unsupported format {ext!r}"
        raise UnsupportedImageFormatError(msg)

"""A class for PIL images as Vectors"""

from PIL import Image
from pathlib import Path
from typing import Sequence


from vec import Vector


class ImageVector(Vector):
    """A class for Images as vectors"""

    size = (300, 300)

    def __init__(self, input):
        """
        The constructor for the ImageVector class which accepts as input an
        image file name or a list of pixels
        """
        if isinstance(input, (Path, str)):
            img = Image.open(input).resize(ImageVector.size)
            if img.mode != "RGB":
                img = img.convert("RGB")
            self.pixels = img.getdata()
        elif isinstance(input, Sequence):
            self.pixels = input

    def image(self):
        """
        Returns a PIL image constructed from the list of pixels stored in the
        class
        """
        img = Image.new("RGB", ImageVector.size)
        img.putdata([(int(r), int(g), int(b)) for (r, g, b) in self.pixels])
        return img

    def put_pixel(self, x, y, rgb):
        _, height = ImageVector.size
        pixel_idx = y * height + x
        self.pixels[pixel_idx] = rgb

    def get_pixel(self, x, y):
        _, height = ImageVector.size
        return self.pixels[y * height + x]

    @classmethod
    def zero(cls):
        total_pixels = cls.size[0] * cls.size[1]
        return ImageVector([(0, 0, 0) for _ in range(total_pixels)])

    def add(self, other):
        return ImageVector(
            [
                (r1 + r2, g1 + g2, b1 + b2)
                for ((r1, g1, b1), (r2, g2, b2)) in zip(
                    self.pixels, other.pixels
                )
            ]
        )

    def scale(self, scalar):
        return ImageVector(
            [(scalar * r, scalar * g, scalar * b) for r, g, b in self.pixels]
        )

    def _repr_png_(self):
        """
        Convenience method to display PIL images inline in Jupyter notebooks
        """
        return self.image()._repr_png_()

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        for (r1, g1, b1), (r2, g2, b2) in zip(self.pixels, other.pixels):
            if r1 != r2 or g1 != g2 or b1 != b2:
                return False
        return True

    def __str__(self):
        """User friendly representation for users of the code"""
        return f"({self.size} image)"

    def __repr__(self):
        """Dev oriented representation for debugging purposes"""
        return f"ImageVector({self.size})"

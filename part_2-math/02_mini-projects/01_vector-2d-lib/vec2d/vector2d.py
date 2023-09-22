"""
A helper library to draw in the 2D plane
"""
from abc import ABC
from typing import Sequence, Optional
from enum import Enum
from math import ceil, floor, sqrt
import matplotlib.pyplot as plt
from matplotlib.pyplot import xlim, ylim
import numpy as np


class Colors(Enum):
    """A few Matplotlib colors using the CN scheme in which
    'C' precedes a number acting as an index into the default
    property cycle (see https://matplotlib.org/stable/users/explain/colors/colors.html).
    """

    BLUE = "C0"
    BLACK = "k"
    RED = "C3"
    GREEN = "C2"
    PURPLE = "C4"
    BROWN = "C5"
    PINK = "C6"
    ORANGE = "C11"
    GRAY = "gray"


class Figure2D(ABC):
    """Abstract base class for all the figures that can be represented
    in the 2D plane.
    """


class Points(Figure2D):
    """Represents a collection of points on the 2D plane, given their
    (x,y) coordinates. The points will be displayed as circles in the
    given color"""

    def __init__(self, *vectors: tuple[int | float, int | float], color=Colors.BLACK) -> None:
        self.vectors = list(vectors)
        self.color = color


class Segment(Figure2D):
    """Represents a segment on the 2D plane, with a start and
    end point. You can also choose the color (blue is the default).
    """

    def __init__(
        self,
        start_point: tuple[int | float, int | float],
        end_point: tuple[int | float, int | float],
        *,
        color: Colors = Colors.BLUE,
    ) -> None:
        self.start_point = start_point
        self.end_point = end_point
        self.color = color


class Polygon(Figure2D):
    """Represents a polygon on the 2D plane, defined by its vertices. You
    can choose the color of the lines using color, whether the figure should be
    filled, and the transparency level with alpha.
    """

    def __init__(
        self,
        *vertices: tuple[int | float, int | float],
        color=Colors.BLUE,
        fill: Optional[Colors] = None,
        alpha=0.4,
    ) -> None:
        self.vertices = vertices
        self.color = color
        self.fill = fill
        self.alpha = alpha


class Arrow(Figure2D):
    """Represents an arrow on the 2D plane, defined by its tip and tail.
    If tail is not provided it is assumed to have its tail in the origin
    of coordinates (0, 0)
    """

    def __init__(self, tip: tuple[int | float, int | float], tail=(0, 0), color=Colors.RED) -> None:
        self.tip = tip
        self.tail = tail
        self.color = color


def extract_vectors(objects: Sequence[Figure2D]) -> tuple[int | float, int | float]:
    """Generator helper function that extract all the vectors
    from a list of objects.

    Args:
        objects (Sequence[Figure2D]): the list of objects whose vectors
        are to be extracted.

    Returns
        tuple[int | float, int | float]: a tuple with the corresponding
            vector coordinates in the 2D plane.
    """
    for obj in objects:
        if isinstance(obj, Segment):
            yield obj.start_point
            yield obj.end_point
        elif isinstance(obj, Points):
            for v in obj.vectors:  # pylint: disable=invalid-name
                yield v
        elif isinstance(obj, Polygon):
            for v in obj.vertices:  # pylint: disable=invalid-name
                yield v
        elif isinstance(obj, Arrow):
            yield obj.tip
            yield obj.tail
        else:
            raise TypeError(f"Unrecognized object {type(obj)}")


def draw(
    *objects: Sequence[Figure2D],
    origin=True,
    axes=True,
    grid=(1, 1),
    nice_aspect_ratio=True,
    width=6,
    save_as: str = None,
):
    """Draws the given objects as a Matplotlib object with the given configuration

    Args:
        objects (Sequence[Figure2D]): the list of figures to be displayed in the plot.
        origin (bool): whether to show or hide the origin of coordinates.
            Default is to show the origin (True).
        axes (bool): whether to show the x- and y-coordinate axes.
            Default is to show the axes (True).
        grid (tuple[int | float, int | float]): sets the frequency for the ticks in the plot
            for x- and y- axes. Default is (1, 1) meaning that you will find a tick per unit
            in both x- and y- axes.
        nice_aspect_ratio (bool): whether to adjust the aspect ratio, so that a square of side
            one is displayed as a square, instead of as a rectangle.
            Default is True.
        width (int | float): the width of the plot. The larger this number, the bigger
            the plot. Default is 6 which is OK for most monitors and 2D drawings.
        save_as (str): absolute path of the file to be created with the plot, or None
            if no file is to be created.
    """
    all_vectors = list(extract_vectors(objects))  # Get all coordinates
    xs, ys = zip(*all_vectors)  # pylint: disable=invalid-name
    max_x, max_y, min_x, min_y = max(0, *xs), max(0, *ys), min(0, *xs), min(0, *ys)

    if grid:
        x_padding = max(ceil(0.05 * (max_x - min_x)), grid[0])
        y_padding = max(ceil(0.05 * (max_y - min_y)), grid[1])

        plt.xlim(
            floor((min_x - x_padding) / grid[0]) * grid[0],
            ceil((max_x + x_padding) / grid[0]) * grid[0],
        )
        plt.ylim(
            floor((min_y - y_padding) / grid[1]) * grid[1],
            ceil((max_y + y_padding) / grid[1]) * grid[1],
        )

    if origin:
        plt.scatter([0], [0], color=Colors.BLACK.value, marker="x")

    if grid:
        plt.gca().set_xticks(np.arange(plt.xlim()[0], plt.xlim()[1], grid[0]))
        plt.gca().set_yticks(np.arange(plt.ylim()[0], plt.ylim()[1], grid[1]))
        plt.grid(True)
        plt.gca().set_axisbelow(True)

    if axes:
        plt.gca().axhline(linewidth=2, color=Colors.BLACK.value)
        plt.gca().axvline(linewidth=2, color=Colors.BLACK.value)

    for obj in objects:
        if isinstance(obj, Segment):
            x1, y1 = obj.start_point  # pylint: disable=invalid-name
            x2, y2 = obj.end_point  # pylint: disable=invalid-name
            plt.plot([x1, x2], [y1, y2], color=obj.color.value)
        elif isinstance(obj, Points):
            xs = [v[0] for v in obj.vectors]  # pylint: disable=invalid-name
            ys = [v[1] for v in obj.vectors]  # pylint: disable=invalid-name
            plt.scatter(xs, ys, color=obj.color.value)
        elif isinstance(obj, Polygon):
            for i in range(0, len(obj.vertices)):  # pylint: disable=consider-using-enumerate
                x1, y1 = obj.vertices[i]  # pylint: disable=invalid-name
                x2, y2 = obj.vertices[(i + 1) % len(obj.vertices)]  # pylint: disable=invalid-name
                plt.plot([x1, x2], [y1, y2], color=obj.color.value)
            if obj.fill:
                xs = [v[0] for v in obj.vertices]  # pylint: disable=invalid-name
                ys = [v[1] for v in obj.vertices]  # pylint: disable=invalid-name
                plt.gca().fill(xs, ys, obj.fill.value, alpha=obj.alpha)
        elif isinstance(obj, Arrow):
            tip, tail = obj.tip, obj.tail
            tip_length = (xlim()[1] - xlim()[0]) / 20.0
            length = sqrt((tip[1] - tail[1]) ** 2 + (tip[0] - tail[0]) ** 2)
            new_length = length - tip_length
            new_y = (tip[1] - tail[1]) * (new_length / length)
            new_x = (tip[0] - tail[0]) * (new_length / length)
            plt.gca().arrow(
                tail[0],
                tail[1],
                new_x,
                new_y,
                head_width=tip_length / 1.5,
                head_length=tip_length,
                fc=obj.color.value,
                ec=obj.color.value,
            )

        else:
            raise TypeError(f"Unrecognized object {type(obj)}")

    if nice_aspect_ratio:
        coords_height = ylim()[1] - ylim()[0]
        coords_width = xlim()[1] - xlim()[0]
        plt.gcf().set_size_inches(width, width * coords_height / coords_width)

    if save_as:
        plt.savefig(save_as)

    plt.show()

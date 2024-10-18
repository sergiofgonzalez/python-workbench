# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "vec2d",
# ]
# ///
from vec2d.graph import (
    Arrow,
    Colors,
    LineStyles,
    Points,
    Polygon,
    Segment,
    draw,
)
from vec2d.math import add

# Testing the blending
asteroid_points = [
    (1, 5),
    (2, 3),
    (4, 2),
    (6, 2),
    (7, 4),
    (6, 6),
    (4, 6),
    (2, 7),
]

draw(
    Segment((0, 10), (10, 0), color=Colors.BLUE),
    Segment((0, 10), (6, 0), color=Colors.RED),
    Polygon(*asteroid_points, color=Colors.GREEN, fill=Colors.GREEN, alpha=0.2),
)

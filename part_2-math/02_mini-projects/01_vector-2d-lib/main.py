"""
Sample program illustrating how to use the vec2d API
"""
from vec2d import Colors, Segment, Points, Polygon, Arrow, draw

if __name__ == "__main__":
    draw(
        Segment((0, 3), (5, 3), color=Colors.ORANGE),
        Points((0, 3), (5, 3), color=Colors.BLUE),
        Polygon((3, 1), (6, 3), (5, 1), fill=Colors.PINK),
        Arrow((5, 3), color=Colors.ORANGE),
        Arrow((3, 1), (5, 3), color=Colors.PINK)
        )

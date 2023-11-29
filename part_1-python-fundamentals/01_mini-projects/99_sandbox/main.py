from vec2d.math import add
from vec2d.graph import draw, Arrow, Colors, LineStyles

u = (2, 0)
v = (1, 3)

draw(
    Arrow(u, color=Colors.ORANGE),
    Arrow(v, color=Colors.PINK, linestyle=LineStyles.LOOSELY_DASHED),
    Arrow(add(u, v), color=Colors.BLUE)
)
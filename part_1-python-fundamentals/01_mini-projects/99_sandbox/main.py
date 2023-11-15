"""
Sample program illustrating how to use the vec3d library API
"""
from vec3d.graph import (
    Arrow3D,
    Colors3D,
    Points3D,
    draw3d,
)

from vec3d.math import cross, subtract

u = (3, -2, 2)
v = (2, 4, 3)

draw3d(
    Arrow3D(u, color=Colors3D.RED),
    Arrow3D(v, color=Colors3D.CYAN),
    Arrow3D(cross(u, v), color=Colors3D.PURPLE),
    Points3D(u, color=Colors3D.RED),
    Points3D(v, color=Colors3D.CYAN),
    Points3D(cross(u, v), color=Colors3D.PURPLE),
    elev=15
)
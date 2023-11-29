"""
Sample program illustrating how to use the vec3d library API
"""
from vec3d.graph import (
    Arrow3D,
    Colors3D,
    LineStyles3D,
    Points3D,
    Segment3D,
    Box3D,
    draw3d,
    Polygon3D
)

from vec3d.math import cross, subtract

import numpy as np

if __name__ == "__main__":
    # # drawing an empty 3D showing only the axes
    # draw3d()

    # # drawing an empty 3D showing only the origin (the perspective is tricky)
    # draw3d(origin=True, axes=False)

    # drawing vector (4, 3, 0) in purple
    # draw3d(
    #     Arrow3D((4, 3, 0), color=Colors.PURPLE),
    #     axes=True
    # )

    # # Draw a couple of Points in the 3D space on a slightly larger canvas
    # draw3d(
    #     Points3D((2, 2, 2), (-1, -2, -2)),
    #     width=8
    # )

    # Draw a couple of Red Points in the 3D space and save the pictue
    # draw3d(
    #     Points3D((2, 2, 2), (-1, -2, -2)),
    #     save_as="couple-points.png"
    # )

    # Draw a Segment in the 3D space in blue using a solid linestyle
    # draw3d(
    #     Segment3D(
    #         (2, 2, 2),
    #         (1, -2, -2),
    #         color=Colors3D.BLUE,
    #         linestyle=LineStyles3D.SOLID,
    #     )
    # )

    # Draw a Box3D which helps to visualize things
    # point = (2, 2, 2)
    # draw3d(
    #     Box3D(*point),
    #     Points3D(point)
    # )

    # Draw a few of points with depthshade
    # Note that initially, the farthest point is dimmed in gray
    # draw3d(
    #     Points3D((1, 1, 1), (2, 2, 2), (5, 5, 5)),
    #     depthshade=False
    # )

    # Draw a Polygon3D
    # draw3d(
    #     Polygon3D((1, 0, 0), (0, 1, 0), (0, 0, 1))
    # )

    # Playing with some draw3d parameters: azim
    # draw3d(
    #     Box3D(2, 2, 2),
    #     azim=30 # 30 degrees of camera rotation about the vertical axis
    # )

    # # Playing with some draw3d parameters: elev
    # draw3d(
    #     Box3D(2, 2, 2),
    #     elev=74 # 74 degrees of elevation
    # )

    # Playing with some draw3d parameters: xlim, ylim, zlim
    # draw3d(
    #     Box3D(2, 2, 2),
    #     xlim=(0, 20), ylim=(0, 20), zlim=(0, 20)
    # )

    # Playing with some draw3d parameters: xticks, yticks, zticks with numpy
    # draw3d(
    #     Box3D(2, 2, 2),
    #     xticks=np.arange(-3, 3, step=0.5),
    #     yticks=np.arange(-3, 3, step=0.5),
    #     zticks=np.arange(-3, 3, step=0.5)
    # )


    # draw3d(
    #     Points3D((2, 2, 2), (1, -2, -2)),
    #     Arrow3D((2, 2, 2)),  # default is RED
    #     Arrow3D((1, -2, -2), color=Colors3D.BLUE),
    #     Segment3D((2, 2, 2), (1, -2, -2)),
    #     Box3D(2, 2, 2),
    #     Box3D(1, -2, -2)
    # )

    # Finding the right perspective (those vectors are perpendicular)
    # draw3d(
    #     Arrow3D((1, 2, -1), color=Colors3D.RED),
    #     Arrow3D((3, 0, 3), color=Colors3D.BLUE),
    #     elev=10
    # )

    # draw3d(
    #     Arrow3D((2, 3, 0), color=Colors3D.RED),
    #     Arrow3D((4, 5, 0), color=Colors3D.BLUE),
    #     Points3D((2, 3, 0), (4, 5, 0)),
    #     elev=15
    # )

    # Finding a good visualization for the cross product
    # u = (3, -2, 2)
    # v = (2, 4, 3)

    # draw3d(
    #     Arrow3D(u, color=Colors3D.RED),
    #     Arrow3D(v, color=Colors3D.CYAN),
    #     Arrow3D(cross(u, v), color=Colors3D.PURPLE),
    #     Points3D(u, color=Colors3D.RED),
    #     Points3D(v, color=Colors3D.CYAN),
    #     Points3D(cross(u, v), color=Colors3D.PURPLE),
    #     elev=15
    # )

    # finding a good visualization for an octahedron face
    # points = [
    #     (1, 0, 0), (0, 1, 0), (0, 0, 1),
    #     (-1, 0, 0), (0, -1, 0), (0, 0, -1),
    # ]

    # edges = [
    #     [(0, 0, 1), (-1, 0, 0)],
    #     [(0, 0, 1), (0, -1, 0)],
    # ]


    # arrows = [Arrow3D(tip, tail, color=Colors3D.BLUE) for tail, tip in edges]

    # draw3d(
    #     Points3D(*points, color=Colors3D.BLUE),
    #     *arrows,
    #     Segment3D((-1, 0, 0), (0, -1, 0)),
    #     elev=10,
    #     zticks=[-1, 0, 1],
    #     xticks=[-1, 0, 1],
    #     yticks=[-1, 0, 1]
    # )

    # Finding a good visualization for a whole octahedron
    # edges = [
    #     [(0, 0, 1), (1, 0, 0)],
    #     [(0, 0, 1), (0, 1, 0)],
    #     [(0, 0, 1), (-1, 0, 0)],
    #     [(0, 0, 1), (0, -1, 0)],
    #     [(0, 0, -1), (1, 0, 0)],
    #     [(0, 0, -1), (0, 1, 0)],
    #     [(0, 0, -1), (-1, 0, 0)],
    #     [(0, 0, -1), (0, -1, 0)],
    #     [(1, 0, 0), (0, 1, 0)],
    #     [(0, 1, 0), (-1, 0, 0)],
    #     [(-1, 0, 0), (0, -1, 0)],
    #     [(0, -1, 0), (1, 0, 0)]
    # ]
    # vertices = set([vertex for edge in edges for vertex in edge])

    # segments = [Segment3D(start, end, color=Colors3D.BLUE) for start, end in edges]
    # points = Points3D(*vertices, color=Colors3D.CYAN)

    # draw3d(
    #     *segments,
    #     points,
    # )

    # Finding a good viz for an octahedron face

    # v1 = (0, 1, 0)
    # v2 = (1, 0, 0)
    # v3 = (0, 0, 1)

    # draw3d(
    #     Arrow3D(v1, color=Colors3D.GRAY),
    #     Arrow3D(v2, color=Colors3D.GRAY),
    #     Arrow3D(v3, color=Colors3D.GRAY),
    #     Arrow3D(v2, v1, color=Colors3D.BLUE),
    #     Arrow3D(v3, v1, color=Colors3D.BLUE),
    #     Segment3D(v2, v3, color=Colors3D.BLUE),
    #     Arrow3D(cross(subtract(v2, v1), subtract(v3, v1)), color=Colors3D.ORANGE),
    # )

    # Finding a good visualization for a 3D rotation
    draw3d(
        Arrow3D((.5, .5, 2), color=Colors3D.BLUE),
        Arrow3D((-.5, .5, 2), color=Colors3D.BLUE, linestyle=LineStyles3D.LOOSELY_DASHED),
        Points3D((.5, .5, 2)),
        Points3D((-.5, .5, 2)),
        xticks=[-1, 0, 1],
        yticks=[-1, 0, 1],
        zticks=[-1, 0, 1],

        elev=12
    )
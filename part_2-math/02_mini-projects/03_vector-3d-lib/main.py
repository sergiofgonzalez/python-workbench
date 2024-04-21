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

from vec3d.math import cross, subtract, add, scale
from collections import namedtuple

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
    # draw3d(
    #     Arrow3D((.5, .5, 2), color=Colors3D.BLUE),
    #     Arrow3D((-.5, .5, 2), color=Colors3D.BLUE, linestyle=LineStyles3D.LOOSELY_DASHED),
    #     Points3D((.5, .5, 2)),
    #     Points3D((-.5, .5, 2)),
    #     xticks=[-1, 0, 1],
    #     yticks=[-1, 0, 1],
    #     zticks=[-1, 0, 1],

    #     elev=12
    # )

    # Finding a good visualization for a 3D sum vector and its projection
    # u = (2, -3, 1)
    # v = (3, 2, 2)
    # u_p = (2, -3, 0)
    # v_p = (3, 2, 0)

    # draw3d(
    #     Arrow3D(u, color=Colors3D.BLUE),
    #     Arrow3D(v, color=Colors3D.RED),
    #     # Arrow3D(add(u, v), u, color=Colors3D.RED, linestyle=LineStyles3D.LOOSELY_DASHED),
    #     # Arrow3D(add(u, v), v, color=Colors3D.BLUE, linestyle=LineStyles3D.LOOSELY_DASHED),
    #     Arrow3D(add(u, v), color=Colors3D.PURPLE),
    #     Arrow3D(u_p, color=Colors3D.BLUE),
    #     Arrow3D(v_p, color=Colors3D.RED),
    #     Arrow3D(add(u_p, v_p), u_p, color=Colors3D.RED, linestyle=LineStyles3D.DOTTED),
    #     Arrow3D(add(u_p, v_p), v_p, color=Colors3D.BLUE, linestyle=LineStyles3D.DOTTED),
    #     Arrow3D(add(u_p, v_p), color=Colors3D.PURPLE, linestyle=LineStyles3D.DOTTED),
    #     Arrow3D(u_p, u, color=Colors3D.GRAY, linestyle=LineStyles3D.DENSELY_DOTTED),
    #     Arrow3D(v_p, v, color=Colors3D.GRAY, linestyle=LineStyles3D.DENSELY_DOTTED),
    #     Arrow3D(add(u_p, v_p), add(u, v), color=Colors3D.GRAY, linestyle=LineStyles3D.DENSELY_DOTTED),
    #     elev=15,
    #     azim=-95,
    # )

    # Finding a good visualization for 2 non-parallel vectors in 3D that span a plane
    # s1 = np.linspace(-5, 5, 25)
    # s2 = np.linspace(-5, 5, 25)

    # u = (1, 0, 1)
    # v = (0, -2, 1)

    # s1s = np.linspace(-5, 5, 15)
    # s2s = np.linspace(-5, 5, 15)

    # points = [add(scale(s1, u), scale(s2, v)) for s1 in s1s for s2 in s2s]

    # draw3d(
    #     Points3D(*points, color=Colors3D.BLUE),
    #     Arrow3D(u, color=Colors3D.BLACK),
    #     Arrow3D(v, color=Colors3D.BLACK),
    # )

# Finding a good visualization for a 3D plane
    # plane_point = (0, 0, 1.2)
    # perpendicular_v = (-1, 2, 5)


    # def get_plane_points_fn(perpendicular_v, plane_point):
    #     a, b, c = perpendicular_v
    #     x0, y0, z0 = plane_point
    #     def new_fn(x, y):
    #         return (x, y, (a * x0 + b * y0 + c * z0 - a * x - b * y) / c)
    #     return new_fn

    # plane_fn = get_plane_points_fn(perpendicular_v, plane_point)
    # xs = np.linspace(-5, 5, 15)
    # ys = np.linspace(-5, 5, 15)

    # draw3d(
    #     Points3D(plane_point),
    #     Points3D(*[plane_fn(x, y) for x in xs for y in ys], color=Colors3D.BLUE),
    #     Arrow3D(plane_fn(xs[3], ys[3]), plane_point, color=Colors3D.BLACK),
    #     Arrow3D(perpendicular_v, plane_point, color=Colors3D.BLACK),
    #     elev=9,
    #     azim=155,
    # )

    # Finding a good visualization for two intersecting planes
    # plane1_point = (0, 0, 1.2)
    # perpendicular1_v = (-1, 2, 5)

    # plane2_point = (2, 2, 2)
    # perpendicular2_v = (2, 0, 3)

    # plane3_point = (0, 0, 0)
    # perpendicular3_v = (0, 0, 1)

    # def get_plane_points_fn(perpendicular_v, plane_point):
    #     a, b, c = perpendicular_v
    #     x0, y0, z0 = plane_point
    #     def new_fn(x, y):
    #         return (x, y, (a * x0 + b * y0 + c * z0 - a * x - b * y) / c)
    #     return new_fn

    # plane1_fn = get_plane_points_fn(perpendicular1_v, plane1_point)
    # plane2_fn = get_plane_points_fn(perpendicular2_v, plane2_point)
    # plane3_fn = get_plane_points_fn(perpendicular3_v, plane3_point)

    # xs = np.linspace(-5, 5, 15)
    # ys = np.linspace(-5, 5, 15)

    # draw3d(
    #     Points3D(*[plane1_fn(x, y) for x in xs for y in ys], color=Colors3D.BLUE),
    #     Points3D(*[plane2_fn(x, y) for x in xs for y in ys], color=Colors3D.GREEN),
    #     Points3D(*[plane3_fn(x, y) for x in xs for y in ys], color=Colors3D.RED),
    #     elev=15,
    #     azim=45,
    # )

    # Finding a good plane intersection visualization
    # import matplotlib.pyplot as plt
    # import numpy as np
    # from mpl_toolkits import mplot3d

    # def plane_1(x, y):
    #     return x + y + 1

    # def plane_2(x, y):
    #     return 2 * y - 3

    # def plane_3(x, y):
    #     return 2 - x

    # xs = np.linspace(-6, 6, 25)
    # ys = np.linspace(-6, 6, 25)

    # planes = [plane_1, plane_2, plane_3]

    # fig = plt.figure()
    # ax = plt.axes(projection="3d")

    # for plane in planes:
    #     X, Y = np.meshgrid(xs, ys)
    #     Z = plane(X, Y)
    #     ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap="binary", edgecolor="none", alpha=0.6)


    # ax.set_xlabel("x")
    # ax.set_ylabel("y")
    # ax.set_zlabel("z")
    # ax.set_title("Three planes")
    # ax.view_init(33, 33)

    # plt.show()

    # finding a good visualization for three intersecting planes
    # def plane_1(x, y):
    #     return (x, y, x + y + 1)

    # def plane_2(x, y):
    #     return (x, y, 2 * y - 3)

    # def plane_3(x, y):
    #     return (x, y, 2 - x)

    # xs = np.linspace(-5, 5, 15)
    # ys = np.linspace(-5, 5, 15)

    # draw3d(
    #     Points3D(*[plane_1(x, y) for x in xs for y in ys], color=Colors3D.BLUE),
    #     Points3D(*[plane_2(x, y) for x in xs for y in ys], color=Colors3D.GREEN),
    #     Points3D(*[plane_3(x, y) for x in xs for y in ys], color=Colors3D.RED),
    #     Points3D((-1, 3, 3), color=Colors3D.BLACK),
    #     elev=18,
    #     azim=45,
    # )

    # Finding a good visualization for a 3D trajectory


    Kinematics = namedtuple("Kinematics", "times, positions, velocities, accelerations")

    def get_kinematics_euler(t0, s0, v0, a0, t_end, steps):
        t = t0
        s = s0
        v = v0
        a = a0
        dt = (t_end - t0) / steps

        times = [t]
        positions = [s]
        velocities = [v]
        accelerations = [a]
        for _ in range(steps):
            t += dt
            s = add(s, scale(dt, v))
            v = add(v, scale(dt, a))

            times.append(t)
            positions.append(s)
            velocities.append(v)
            accelerations.append(a)

        return Kinematics(times, positions, velocities, accelerations)


    kinematics = get_kinematics_euler(
        t0=0,
        s0=(0, 0, 0),
        v0=(1, 2, 0),
        a0=(0, -1, 1),
        t_end=10,
        steps=10
    )

    draw3d(
        Points3D(*kinematics.positions)
    )
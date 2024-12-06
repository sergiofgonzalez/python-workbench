from math import cos, pi, sin

import matplotlib.pyplot as plt
import numpy as np


def flat_ground(x, y):
    return 0


def ridge(x, y):
    return (x**2 - 5 * y**2) / 2500


def trajectory3d(
    theta_deg, phi_deg, speed=20, height=0, dt=0.011, g=-9.81, elevation=flat_ground
):
    vx = speed * cos(pi * theta_deg / 180) * cos(pi * phi_deg / 180)
    vy = speed * cos(pi * theta_deg / 180) * sin(pi * phi_deg / 180)
    vz = speed * sin(pi * theta_deg / 180)
    t, x, y, z = 0, 0, 0, height
    ts, xs, ys, zs = [t], [x], [y], [z]
    while z >= elevation(x, y):
        t += dt
        vz += g * dt
        x += vx * dt
        y += vy * dt
        z += vz * dt
        ts.append(t)
        xs.append(x)
        ys.append(y)
        zs.append(z)
    return ts, xs, ys, zs


def plot_trajectory3d(traj):
    fig = plt.figure()
    fig.set_size_inches(7, 7)
    ax = plt.axes(projection="3d")

    ax.plot(traj[1], traj[2], traj[3])


def plot_trajectories_3d(
    *trajs, elevation=flat_ground, bounds=None, zbounds=None, shadows=False
):
    fig = plt.figure()
    fig.set_size_inches(7, 7)
    ax = plt.axes(projection="3d")

    if not bounds:
        xmin = min([x for traj in trajs for x in traj[1]])
        xmax = max([x for traj in trajs for x in traj[1]])
        ymin = min([y for traj in trajs for y in traj[2]])
        ymax = max([y for traj in trajs for y in traj[2]])

        padding_x = 0.1 * (xmax - xmin)
        padding_y = 0.1 * (ymax - ymin)

        xmin -= padding_x
        xmax += padding_x
        ymin -= padding_y
        ymax += padding_y
    else:
        xmin, xmax, ymin, ymax = bounds

    # draw axis to set context
    ax.plot([xmin, xmax], [0, 0], [0, 0], color="k")
    ax.plot([0, 0], [ymin, ymax], [0, 0], color="k")

    g = np.vectorize(elevation)
    ground_x = np.linspace(xmin, xmax, 20)
    ground_y = np.linspace(ymin, ymax, 20)
    ground_x, ground_y = np.meshgrid(ground_x, ground_y)
    ground_z = g(ground_x, ground_y)
    ax.plot_surface(
        ground_x,
        ground_y,
        ground_z,
        cmap="coolwarm",
        alpha=0.5,
        linewidth=0,
        antialiased=True,
    )

    for traj in trajs:
        ax.plot(traj[1], traj[2], traj[3])
        if shadows:
            ax.plot(
                [traj[1][0], traj[1][-1]],
                [traj[2][0], traj[2][-1]],
                [0, 0],
                color="gray",
                linestyle="dashed",
            )

        if zbounds:
            ax.set_zlim(*zbounds)

    plt.show()


if __name__ == "__main__":
    plot_trajectories_3d(
        trajectory3d(20, 240, elevation=ridge),
        bounds=[-40, 0, -40, 0],
        elevation=ridge,
        shadows=True,
    )

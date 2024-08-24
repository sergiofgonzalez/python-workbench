"""
Plotting functions for cannonballsim
"""

from typing import List

import matplotlib.pyplot as plt

from cannonballsim.physics import trajectory


def plot_trajectories(*trajectories: tuple, show_seconds=False):
    """
    Plot the trajectories of cannonballs on a 2D plot.

    Args:
        trajectories (tuple): Tuple containing the time, x, and z (height)
            coordinates of the trajectory, and a label for the trajectory that
            can be used to identify it on the plot.

        show_seconds (bool): If True, mark the position of the cannonball in the
            trajectory every second.
    """
    _, ax = plt.subplots()
    ax.grid(True)
    ax.set_xlabel("x")
    ax.set_ylabel("z")

    ax.axhline(y=0, color="k")
    ax.axvline(x=0, color="k")

    for ts, xs, zs, label in trajectories:
        ax.plot(xs, zs, label=label)

        if show_seconds:
            second_indices = []
            second_mark = 0
            for i, t in enumerate(ts):
                if t >= second_mark:
                    second_indices.append(i)
                    second_mark += 1
            ax.scatter(
                [xs[i] for i in second_indices],
                [zs[i] for i in second_indices],
            )

    ax.legend()
    plt.show()


def plot_trajectory_metric(
    metric: callable,
    angles_deg: List[float],
    plot_label: str,
    metric_label: str,
    **kwargs
):
    """
    Plot a metric of a trajectory as a function of the launch angle.

    Args:
        metric (function): Function that takes a trajectory as input and returns
            a scalar value.

        angles_deg (list): List of launch angles in degrees.

        plot_label (str): Label for the plot.

        metric_label (str): Label for the y-axis of the plot.

        **kwargs: Additional keyword arguments to pass to the trajectory
            function.
    """

    _, ax = plt.subplots()
    ax.grid(True)
    ax.set_xlabel("$ \\theta (°) $")
    ax.set_ylabel(metric_label)

    ax.axhline(y=0, color="k")
    ax.axvline(x=0, color="k")

    ax.scatter(
        angles_deg,
        [metric(trajectory(theta_deg, **kwargs)) for theta_deg in angles_deg],
        label=plot_label,
    )

    ax.legend()
    plt.show()

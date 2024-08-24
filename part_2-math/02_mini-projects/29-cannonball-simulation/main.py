"""Illustrates how to use the cannonballsim module"""

from cannonballsim import (
    max_height,
    plot_trajectories,
    plot_trajectory_metric,
    trajectory,
)

if __name__ == "__main__":
    # # Plot the trajectories of cannonballs launched at different angles
    # plot_trajectories(
    #     trajectory(20),
    #     trajectory(45),
    #     trajectory(60),
    #     trajectory(80),
    # )

    # # Plot the trajectories of cannonballs launched at different angles, showing
    # # the position of the cannonball every second
    # plot_trajectories(
    #     trajectory(20),
    #     trajectory(45),
    #     trajectory(60),
    #     trajectory(80),
    #     show_seconds=True,
    # )

    # # Plot a metric of the trajectory as a function of the launch angle
    # plot_trajectory_metric(
    #     metric=max_height,
    #     angles_deg=range(0, 181, 5),
    #     plot_label="Maximum height",
    #     metric_label="Height (m)",
    # )

    # Plot a metric of the trajectory as a function of the launch angle
    # passing initial values to the trajectory function
    plot_trajectory_metric(
        metric=max_height,
        angles_deg=range(0, 181, 5),
        plot_label="Maximum height",
        metric_label="Height (m)",
        height=10,
    )

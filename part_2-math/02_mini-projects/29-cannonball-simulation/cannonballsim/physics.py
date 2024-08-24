"""
Physics module for cannonball simulation that includes the function to
calculate the trajectory of a cannonball given initial conditions along with the
functions to calculate the metrics of the trajectory such as the maximum height,
range, and hang time.
"""

from math import cos, pi, sin


def trajectory(
    theta_deg: float,
    speed: float = 20,
    height: float = 0,
    dt: float = 0.01,
    g: float = -9.81,
):
    """
    Calculate the trajectory of a cannonball given initial conditions.

    Args:
        theta_deg (float): Launch angle in degrees.
        speed (float): Launch speed in m/s.
        height (float): Launch height in meters.
        dt (float): Time step in seconds.
        g (float): Acceleration due to gravity in m/s^2.

    Returns:
        tuple: Tuple containing the time, x, and z (height) coordinates of the
                trajectory, and a label for the trajectory describing the
                initial values used for the simulation.
    """
    vx = speed * cos(pi * theta_deg / 180)
    vz = speed * sin(pi * theta_deg / 180)
    t, x, z = 0, 0, height
    ts, xs, zs = [t], [x], [z]
    while z >= 0:
        t += dt
        vz += g * dt
        x += vx * dt
        z += vz * dt
        ts.append(t)
        xs.append(x)
        zs.append(z)

    label = f"Trajectory for {theta_deg}°"
    if speed != 20:
        label += f" and speed {speed}"
    if height != 0:
        label += f" and height {height}"

    return ts, xs, zs, label


def landing_position(traj: tuple) -> float:
    """
    Calculate the landing position of a cannonball trajectory.

    Args:
        traj (tuple): Tuple containing the time, x, and z (height) coordinates
        of the trajectory.
    """
    return traj[1][-1]


def max_height(traj: tuple) -> float:
    """
    Calculate the maximum height of a cannonball trajectory.

    Args:
        traj (tuple): Tuple containing the time, x, and z (height) coordinates
        of the trajectory.
    """
    return max(traj[2])


def hang_time(traj: tuple) -> float:
    """
    Calculate the hang time of a cannonball trajectory.

    Args:
        traj (tuple): Tuple containing the time, x, and z (height) coordinates
        of the trajectory.
    """
    return traj[0][-1]

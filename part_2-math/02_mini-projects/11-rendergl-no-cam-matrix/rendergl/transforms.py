"""
Vector transformations
"""
from typing import Callable, Tuple

from vec2d.math import to_cartesian, to_polar
from vec3d.math import add, scale


def polygon_map(transformation, polygons):
    """Generic function that applies the given transformation to all the
    vertices found in the given polygons.

    Args:
        transformation (Callable[tuple[float, float, float],
            Tuple[flloat, float, float]]): a function that takes a vector and
            returns a transformed vector.
        polygons (list[list[tuple(float, float, float)]]): a list of polygons.
            Each polygon is a triangle with three vertices, so polygons is
            effectively a list of lists of vertices.

    Returns:
        (list[list[tuple(float, float, float)]]): the transformed polygons. That
            is, a list of list of transformed vertices.
    """
    return [
        [transformation(vertex) for vertex in triangle] for triangle in polygons
    ]


def scale_by(scalar):
    """Generic function that takes an scalar value and returns a transformation
    function that scales each of the vectors/vertices of a given 3D shape by the
    given value.

    Args:
        scalar (float): the scaling factor that will be ultimately applied to
            all the vectors/vertices of the 3D shape.

    Returns:
        (Callable[tuple[float, float, float], tuple[float, float, float]]): a
            transformation function that when invoked with a vector/vertex will
            scale it by the configured scalar.

    """

    def new_fn(v):
        return scale(scalar, v)

    return new_fn


def translate_by(translation):
    """Generic function that takes a translation vector and returns a
    transformation function that translates each of the vectors/vertices of a
    given 3D shape by the given translation vector.

    Args:
        translation (tuple[float, float, float]): the translation vector that
        will be ultimately applied to all the vectors/vertices of the 3D shape.

    Returns:
        (Callable[tuple[float, float, float], tuple[float, float, float]]): a
            transformation function that when invoked with a vector/vertex will
            translate it by the configured translation vector.
    """

    def new_fn(v):
        return add(translation, v)

    return new_fn


def rotate2d(angle: float, vector: tuple[float, float]) -> tuple[float, float]:
    """Takes an angle in radians and a vector of the 2D plane and returns the
    input vector rotated by the given angle counterclockwise
    about the origin if the given angle is positive, or clockwise if the given
    angle is negative.

    Args:
        angle (float): the angle (in radians) that will be used in the rotation.
        vector (tuple[float, float]): the 2D vector to be rotated, given its
        Cartesian coordinates.

    Returns:
        tuple[float, float]: the 2D vector that results from rotating the given
        vector by the given angle.
    """
    l, a = to_polar(vector)
    return to_cartesian((l, a + angle))


def rotate_z(
    angle: float, vector: tuple[float, float, float]
) -> tuple[float, float, float]:
    """
    Rotates a vector the given angle about the z- axis.

    Args:
        angle (float): the angle (in radians) that will be applied in the
            rotation.
        vector (tuple[float, float, float]): the 3D vector to be rotated about
            the z- axis.

    Returns:
        (tuple[float, float, float]): the 3D vector that results from rotating
            the given vector about the z- axis with the specified angle.

    """
    x, y, z = vector
    new_x, new_y = rotate2d(angle, (x, y))
    return new_x, new_y, z


def rotate_z_by(angle: float):
    """Generic function that takes a rotation in radians and returns a
    transformation function that rotates each of the vectors/vertices of a
    given 3D shape by the given angle about the z- axis.

    Args:
        angle (float): the rotation angle that will be ultimately applied to all
            the vectors/vertices of the 3D shape.

    Returns:
        (Callable[tuple[float, float, float], tuple[float, float, float]]): a
            transformation function that when invoked with a vector/vertex will
            rotate the corresponding vector by the configured angle about the z-
            axis.
    """

    def new_fn(v):
        return rotate_z(angle, v)

    return new_fn


def rotate_x(angle, vector):
    """
    Rotates a vector the given angle about the x- axis.

    Args:
        angle (float): the angle (in radians) that will be applied in the
            rotation.
        vector (tuple[float, float, float]): the 3D vector to be rotated about
            the x- axis.

    Returns:
        (tuple[float, float, float]): the 3D vector that results from rotating
            the given vector about the x- axis with the specified angle.

    """
    x, y, z = vector
    new_y, new_z = rotate2d(angle, (y, z))
    return x, new_y, new_z


def rotate_x_by(angle):
    """Generic function that takes a rotation in radians and returns a
    transformation function that rotates each of the vectors/vertices of a
    given 3D shape by the given angle about the x- axis.

    Args:
        angle (float): the rotation angle that will be ultimately applied to all
            the vectors/vertices of the 3D shape.

    Returns:
        (Callable[tuple[float, float, float], tuple[float, float, float]]): a
            transformation function that when invoked with a vector/vertex will
            rotate the corresponding vector by the configured angle about the x-
            axis.
    """

    def new_fn(v):
        return rotate_x(angle, v)

    return new_fn


def rotate_y(angle, vector):
    """
    Rotates a vector the given angle about the y- axis.

    Args:
        angle (float): the angle (in radians) that will be applied in the
            rotation.
        vector (tuple[float, float, float]): the 3D vector to be rotated about
            the y- axis.

    Returns:
        (tuple[float, float, float]): the 3D vector that results from rotating
            the given vector about the y- axis with the specified angle.

    """
    x, y, z = vector
    new_x, new_z = rotate2d(angle, (x, z))
    return new_x, y, new_z


def rotate_y_by(angle):
    """Generic function that takes a rotation in radians and returns a
    transformation function that rotates each of the vectors/vertices of a
    given 3D shape by the given angle about the y- axis.

    Args:
        angle (float): the rotation angle that will be ultimately applied to all
            the vectors/vertices of the 3D shape.

    Returns:
        (Callable[tuple[float, float, float], tuple[float, float, float]]): a
            transformation function that when invoked with a vector/vertex will
            rotate the corresponding vector by the configured angle about the y-
            axis.
    """

    def new_fn(v):
        return rotate_y(angle, v)

    return new_fn


def compose(
    *args: Callable[[Tuple[float, float, float]], Tuple[float, float, float]]
) -> Callable[[Tuple[float, float, float]], Tuple[float, float, float]]:
    """A generic function that takes any positive number of transformation
    functions and returns the transformation that results from composing them.
    Note that the functions are applied in reversed order: the first function is
    the last being applied, so that `compose(scale, rotate)` first applies the
    rotation and then the scaling.

    Args:
        args (Callable[[Tuple[float, float, float]], Tuple[float, float, float]]): A variadic number of transformation functions whose composition is to be returned.

    Returns:
        (Callable[[Tuple[float, float, float]], Tuple[float, float, float]]): The transformation function that results from applying the transformation functions passed as arguments in reversed order.
    """

    def new_transformation_fn(
        v: Tuple[float, float, float]
    ) -> Tuple[float, float, float]:
        result = v
        for fn in reversed(args):
            result = fn(result)
        return result

    return new_transformation_fn

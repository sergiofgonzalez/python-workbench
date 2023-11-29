"""
Vector transformations
"""
from vec2d.math import rotate
from vec3d.math import add, scale


def polygon_map(transformation, polygons):
    return [
        [transformation(vertex) for vertex in triangle] for triangle in polygons
    ]


def scale_by(scalar):
    def new_fn(v):
        return scale(scalar, v)

    return new_fn


def rotate_x(angle, vector):
    x, y, z = vector
    new_y, new_z = rotate(angle, [(y, z)])[0]
    return x, new_y, new_z


def rotate_x_by(angle):
    def new_fn(v):
        return rotate_x(angle, v)

    return new_fn


def translate_by(translation):
    def new_fn(v):
        return add(translation, v)

    return new_fn

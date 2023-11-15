from matplotlib import colormaps
from vec2d.graph import Colors, Polygon, draw
from vec3d.math import cross, dot, length, scale, subtract

blues = colormaps.get_cmap("Blues")

# Type alias
IntOrFloat = int | float


def vertices(faces):
    """Return the list of vertices of a 3D shape given their faces

    Args:
        faces: a list of lists of polygons designating the faces of a 3D shape.

    Returns:
        list[IntOrFloat, IntOrFloat, IntOrFloat]: the list of vertices of the 3D
            shape.
    """
    return list(set([vertex for face in faces for vertex in face]))


def component(v, direction):
    """Extracts and returns the part of any 3D vector pointing in the given
    direction.

    Args:
        v (tuple[IntOrFloat, IntOrFloat, IntOrFloat]): the vector whose
            component in the given direction is to be extracted.
        direction (tuple[IntOrFloat, IntOrFloat, IntOrFloat]): a vector
            indicating the direction.

    Returns:
        float: the component of v in the given direction. For example
            component((5, 10, 25), (0, 1, 0)) will return 10.
    """
    return dot(v, direction) / length(direction)


def vector_to_2d(v):
    """Return the projection of a 3D vector on the 2D plane by removing its z
    çcoordinate.

    Args:
        v (tuple[IntOrFloat, IntOrFloat, IntOrFloat]): the 3D vector whose
            projection is to be calculated.

    Returns:
        tuple[IntOrFloat, IntOrFloat]: the 2D vector that results from
            projecting the given 3D vector on the 2D plane.
    """
    return (
        component(v, (1, 0, 0)),
        component(v, (0, 1, 0)),
    )


def face_to_2d(face):
    """Returns the polygon that results from projecting the given face of a 3D
    shape on the 2D plane.

    Args:
        face (list[tuple[IntOrFloat, IntOrFloat, IntOrFloat]]): a face of a 3D
            shape designated by a list of 3D vectors/points.

    Returns:
        list[tuple[IntOrFloat, IntOrFloat]]: a polygon on the 2D plane,
            designated by a list of 2D vectors/points.
    """
    return [vector_to_2d(vertex) for vertex in face]


def unit(v):
    """Returns a vector that lies in the same direction as the one given, but
    scaled so that its length is exactly 1.

    Args:
        v (tuple[IntOrFloat, IntOrFloat, IntOrFloat]): a vector designated byt
            its Cartesian coordinates.

    Returns:
        tuple[IntOrFloat, IntOrFloat, IntOrFloat]: a vector that lies in the
            same direction as the one give, but whose length is 1.
    """
    return scale(1.0 / length(v), v)


def normal(face):
    """Returns the normal vector for any given triangular face. Note that to be
    used in calculating shading, the vertices of the face must be arranged in a
    way that cross(sub(face[1], face[0]), sub(face[2], face[0])) points outwards
    from the 3D face.

    Args:
        face (list[tuple[IntOrFloat, IntOrFloat, IntOrFloat]]): a face of a 3D
            shape designated by a list of 3D vectors/points.

    Returns:
        tuple[IntOrFloat, IntOrFloat, IntOrFloat]: the normal vector, that is, a
            vector that is perpendicular to the given face.
    """
    return cross(subtract(face[1], face[0]), subtract(face[2], face[0]))


def render(faces, light=(1, 2, 3), colormap=blues, lines=None):
    """Renders the 3D shape designated by its faces (a list of triangles) using
    the given light source orientation, colormap, and lines color. The rendering
    strategy consists in projecting each of the faces in the 2D plane and
    adjusting the corresponding fill color for the resulting 2D triangle using
    the face normal vector.

    Args:
        faces (list[tuple[IntOrFloat, IntOrFloat, IntOrFloat]]): a list of lists
            triangles designating the faces of a 3D shape. Note that the
            vertices of each corresponding face must be arranged in a way that
            cross(sub(face[1], face[0]), sub(face[2], face[0])) points outwards
            from the 3D face.

        light ([tuple[IntOrFloat, IntOrFloat, IntOrFloat]): a vector giving the
            light source orientation.

        colormap: a Matplotlib colormap that will be used for shading.

        lines (Colors): the color to be used for delimiting each projected face.
    """
    polygons = []
    for face in faces:
        unit_normal = unit(normal(face))
        if unit_normal[2] > 0:
            fill_color = colormap(1 - dot(unit(normal(face)), unit(light)))
            p = Polygon(*face_to_2d(face), fill=fill_color, color=lines)
            polygons.append(p)
    draw(*polygons, axes=False, origin=False, grid=None)

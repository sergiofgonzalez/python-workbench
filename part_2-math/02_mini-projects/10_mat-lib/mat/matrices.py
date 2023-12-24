"""
Matrix library
"""
from vec3d.math import dot, linear_combination


def multiply_matrix_vector(matrix, vector):
    """Returns the vector that results from multiplying the matrix by the vector

    Args:
        matrix: the matrix as a tuple of tuples of floats.
        vector: the vector as a tuple of floats.

    Returns:
        (tuple[float, float, float]): the vector that results from multiplying
            the matrix by the vector
    """
    return linear_combination(vector, *zip(*matrix))


def matrix_multiply(a, b):
    """Returns the matrix that results from multiplying the matrices given.

    Args:
        a: the first matrix.
        b: the second matrix

    Returns:
        (tuple(tuple[float, float, float])): the matrix that results from
            multiplying the matrices a and b.
    """
    return tuple(tuple(dot(row_v, col_v) for col_v in zip(*b)) for row_v in a)


def std_basis(n):
    """Returns a list with the standard basis vectors for the dimension given

    Args:
        n (int): the number of dimensions of the plane/space whose standard
            basis will be returned.

    Returns:
        (tuple(Tuple[float])): a list with the standard basis vectors
    """
    return [tuple(1 if pos == i else 0 for pos in range(n)) for i in range(n)]


def infer_matrix(n, transformation):
    """Returns the matrix that represents a linear transformation or linear map.

    Args:
        n (int): the number of dimensions of the plane/space of the vectors that
            are sent as input for the transformation.
        transformation (Callable[Tuple[float], Tuple[float]]): a function that
            takes a vector of n dimensions and returns another vector (might) be
            of a different dimension.

    Returns:
        (tuple[Tuple[float]]): the matrix that represents the transformation.
    """
    vectors = std_basis(n)
    m = tuple(transformation(vectors[i]) for i in range(n))
    return tuple(zip(*m))

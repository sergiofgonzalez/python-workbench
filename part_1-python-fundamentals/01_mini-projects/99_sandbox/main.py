from vec3d.math import linear_combination, unit


print(unit((2, 0, 0)))

print(linear_combination([1, 2, 3], (1, 1, 1), (2, 2, 2), (3, 3)))


def multiply_matrix_vector(matrix, vector):
    return linear_combination(vector, *zip(*matrix))

B = (
    (0, 2, 1),
    (0, 1, 0),
    (1, 0, -1),
)

v = (3, -2, 5)

print(multiply_matrix_vector(B, v))
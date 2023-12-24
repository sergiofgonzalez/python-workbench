"""
Simple shakedown for the mat library
"""
from mat import multiply_matrix_vector, matrix_multiply


A = (
    (0, 2, 1),
    (0, 1, 0),
    (1, 0, -1)
)

v = (3, -2, 5)

print(f"multiply_matrix_vector(A, v)={multiply_matrix_vector(A, v)}")

B = (
    (1, 1, 0),
    (1, 0, 1),
    (1, -1, 1)
)

C = (
    (0, 2, 1),
    (0, 1, 0),
    (1, 0, -1)
)

print(f"matrix_multiply(B, C)={matrix_multiply(B, C)}")

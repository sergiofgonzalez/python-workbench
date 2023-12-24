"""
__init__.py for the mat package.
"""
from mat.matrices import (
    infer_matrix,
    matrix_multiply,
    multiply_matrix_vector,
    std_basis,
)

__all__ = [
    "infer_matrix",
    "matrix_multiply",
    "multiply_matrix_vector",
    "std_basis",
]

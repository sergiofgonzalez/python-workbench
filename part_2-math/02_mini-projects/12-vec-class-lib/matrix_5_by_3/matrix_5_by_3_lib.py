"""A class to represent Matrices of 5x3 inheriting from Matrix base class"""
from vecmatrix import Matrix


class Matrix_5_by_3(Matrix):  # pylint: disable=C0103:invalid-name
    @classmethod
    def rows(cls):
        return 5

    @classmethod
    def columns(cls):
        return 3

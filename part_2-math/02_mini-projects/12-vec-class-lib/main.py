"""App entry point"""

import math
from pathlib import Path

from car_for_sale import CarForSale
from coordvec import CoordinateVector
from linearmap_3d_to_5d import LinearMap_3D_to_5D, Vector3D, Vector5D
from matrix_5_by_3 import Matrix_5_by_3
from matrix_5x3 import Matrix5x3
from tests.utils.testutils_vecimg import ImageVectorTestUtils
from vec2 import Vec2
from vec3 import Vec3
from vecfunc import Function
from vecfunc2 import Function2
from vecimg import ImageVector
from veclinfunc import LinearFunction
from vecmatrix import Matrix
from vecpoly import Polynomial
from vecquadfunc import QuadraticFunction

v = Vec2(3, 4)
w = v.add(Vec2(-2, 6))

assert w.x == 1 and w.y == 10

w = v.scale(10)
assert w.x == 30 and w.y == 40


assert w == Vec2(30, 40)


u = Vec2(1, 2)
v = Vec2(3, 4)
w = u + v

print(w.x, w.y)

print(2 * u)
print(u * 2)

print(repr(3 * u))

u = Vec3(1, 2, 3)
v = Vec3(4, 5, 6)

assert 2 * (u + v) == Vec3(10, 14, 18)
print(u + v)
print(repr(u + v))


print(2.0 * (Vec3(1, 0, 0) + Vec3(0, 1, 0)))

print(v - u)


class Vec6(CoordinateVector):
    @classmethod
    def dimension(cls):
        return 6


u = Vec6(1, 2, 3, 4, 5, 6)
v = Vec6(11, 12, 13, 14, 15, 16)

print(Vec6.dimension())
print(Vec6.zero())
# print(u.dimension)

print(repr(u + v))
print(10 * u)

print(-u)

cars = CarForSale.load_cars_from_dataset()
print(cars[0])
print(cars[1])
print(cars[0] + cars[1])

print(Matrix5x3.zero())

m1 = Matrix5x3(
    (
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        (10, 11, 12),
        (13, 14, 15),
    )
)

m2 = Matrix5x3(
    (
        (11, 12, 13),
        (14, 15, 16),
        (17, 18, 19),
        (20, 21, 22),
        (23, 24, 25),
    )
)

print(m1 + m2)
print(2 * m1)
print(m1 == m2)
print(m1 == m1)
print(repr(m1))


## ImageVector

# img_vec = ImageVector("./beach.png")
# img_vec.image().show()

# res = 0.75 * ImageVector("./beach.png") + 0.25 * ImageVector("sunflower.png")
# res.image().show()

# res = 1.5 * ImageVector("sunflower.png")
# res.image().show()

# res = -ImageVector("beach.png")
# res.image().show()

# width, height = ImageVector.size
# white = ImageVector([(255, 255, 255) for _ in range(width * height)])
# white.image().show()

# beach = ImageVector("beach.png")
# beach.image().show()
# res = white - beach
# res.image().show()

## Function

# f = Function(lambda x: x + 5)
# g = Function(math.sin)
# print(f(0))
# print(f(5))

# Function.plot(
#     [f, g, f + g, 3 * f],
#     -10,
#     10,
#     ["f(x) = x + 5", "g(x) = sin(x)", "f+g", r"$3 \cdot f$"],
# )

## Polynomials
# print("======")

# p1 = Polynomial(1, 2, 3)
# p2 = Polynomial(1, 2)

# print(p1._repr_latex_()) # pylint: disable=W0212:protected-access

# print(p1)
# print(p2)

# print(p1 + p2)

# print(2 * p1)

# print(repr(p1))

# print(p1(1))  # 1 + 2 * 1 + 3 * 1^2
# print(p1(2))  # 1 + 2 * 2 + 3 * 2^2

## Function2

# f = Function2(lambda x, y: x + y)
# print(f(1, 2))

# f.plot(xmin=-10, xmax=10, ymin=-10, ymax=10)

# Matrix class
# print("======")

## The matrix base class shouldn't be instantiated
# try:
#     m = Matrix(((1, 2), (3, 4)))
# except TypeError:
#     print("Can't instantiate!")

# m = Matrix_5_by_3(
#     (
#         (1, 2, 3),
#         (4, 5, 6),
#         (7, 8, 9),
#         (10, 11, 12),
#         (13, 14, 15),
#     )
# )

# print(m)
# print(m._repr_latex_())

# print(Matrix5x3.zero())


# Linear_3D_to_5D
# linear_map = LinearMap_3D_to_5D(
#     (
#         (1, 2, 3),
#         (4, 5, 6),
#         (7, 8, 9),
#         (10, 11, 12),
#         (13, 14, 15),
#     )
# )

# print(linear_map)

# v3d = Vector3D(1, 0, 0)

# print(linear_map(v3d))

# print(LinearMap_3D_to_5D.zero())

# Overloading matrix multiplication so that you can use either scalars or
# vectors

# m = Matrix_5_by_3(
#     (
#         (1, 2, 3),
#         (4, 5, 6),
#         (7, 8, 9),
#         (10, 11, 12),
#         (13, 14, 15),
#     )
# )
# print(m * 2)

# v = Vec3(1, 1, 1)
# print(m * v)

# # Overloading vector multiplication is not needed, you can use it right away

# print(2 * v)
# print(m * v)

# What does a random image look like?

# ImageVectorTestUtils.random_vector().image().show()


# # LinearFunction

# f = LinearFunction(2, 3)
# print(f)
# print(repr(f))

# g = LinearFunction(1, 0)
# print(f)

# LinearFunction.plot([f, g, f + g], -10, 10)


# ImageVector (shades of gray)

# width, height = ImageVector.size
# gray = ImageVector([(1, 1, 1) for _ in range(width * height)])

# (191 * gray).image().show()

# QuadraticFunction

# f = QuadraticFunction(1, 2, 3)  # x^2 + 2x + 3
# print(f)
# print(repr(f))
# print(f._repr_latex_())

# g = QuadraticFunction(-1, 1, 0)
# print(g)
# print(repr(g))
# print(g._repr_latex_())

# h = 2 * (f + g)
# print(h)
# print(repr(h))
# print(h._repr_latex_())

# QuadraticFunction.plot([f, g, h], -10, 10)

# Grayscale: mapping 30x30 brightness matrix to a 300x300 pixel image

# Increasing brightness from left-to-right, from top-to-bottom
# brightness_matrix = [
#     [math.floor((256 / 900) * (i * 30 + j)) for j in range(30)]
#     for i in range(30)
# ]

# Checkquered flag
# brightness_matrix = [
#     [0 if (i + j) % 2 == 0 else 255 for j in range(30)] for i in range(30)
# ]

# Increasing brightness from left-to-right, then right-to-left, then left-to-r...
# brightness_matrix = [
#     [math.floor((256 / 900) * (i * 30 + j)) if i % 2 == 0 else math.floor((256 / 900) * (i * 30 + (30 - j))) for j in range(30)]
#     for i in range(30)
# ]


# def get_image_from_brightness_matrix(m):
#     def map_pixel_x_y_to_brightness_rgb(x, y):
#         j = x // 10
#         i = y // 10
#         return (m[i][j], m[i][j], m[i][j])

#     width, height = ImageVector.size

#     return ImageVector(
#         [
#             map_pixel_x_y_to_brightness_rgb(i % 300, i // 300)
#             for i in range(width * height)
#         ]
#     )


# img = get_image_from_brightness_matrix(brightness_matrix)
# img.image().show()

# # Testing the new get_pixel / put_pixel
# for y in range(0, 299, 10):
#     print(f"(x=0, {y=}): {img.get_pixel(0, y)}")
#     img.put_pixel(0, y, (255, 0, 0))

# img.image().show()

# grayscale image
# img_vec = ImageVector("./beach.png")
# img_vec.image().show()

# resulting_grayscale = []
# for pixel in img_vec.pixels:
#     r, g, b = pixel
#     brightness = (r + g + b) / 3
#     resulting_grayscale.append((brightness, brightness, brightness))

# gray_img = ImageVector(
#     [
#         ((r + g + b) / 3, (r + g + b) / 3, (r + g + b) / 3)
#         for r, g, b in img_vec.pixels
#     ]
# )
# gray_img.image().show()

# New checks on image creation

# 1. File that doesn't exist (as a string)
# try:
#     ImageVector("./non-existing.png")
# except Exception as e:  # pylint: disable=W0718:broad-exception-caught
#     print(e)

# # 2. File that doesn't exist (as a Path)
# f = Path("./non-existing.png")
# try:
#     ImageVector(f)
# except Exception as e:  # pylint: disable=W0718:broad-exception-caught
#     print(e)

# # 3. Sending a list of pixels should work
# width, height = ImageVector.size
# img = ImageVector([(50, 50, 50) for _ in range(width * height)])
# img.image().show()

# Getting a 30x30 brightness matrix out of an image
img = ImageVector("./sunflower.png")

brightness_matrix = []
width, height = ImageVector.size
for y in range(0, height, 10):
    brightness_row = []
    for x in range(0, width, 10):
        x_min, x_max = x, x + 10
        y_min, y_max = y, y + 10
        sum_color_val = 0
        for sq_y in range(y_min, y_max):
            for sq_x in range(x_min, x_max):
                r, g, b = img.get_pixel(sq_x, sq_y)
                sum_color_val += r + g + b
        brightness_row.append(
            sum_color_val / (3 * (x_max - x_min) * (y_max - y_min))
        )
    brightness_matrix.append(brightness_row)

print(brightness_matrix)

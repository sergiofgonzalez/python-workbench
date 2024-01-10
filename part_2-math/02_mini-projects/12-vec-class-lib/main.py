"""App entry point"""

from car_for_sale import CarForSale
from coordvec import CoordinateVector
from matrix_5x3 import Matrix5x3
from vec2 import Vec2
from vec3 import Vec3

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

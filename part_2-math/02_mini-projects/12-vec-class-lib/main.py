"""App entry point"""

from coordvec import CoordinateVector
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


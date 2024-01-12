"""App entry point"""
from coordvec import CoordinateVector


class Vec6(CoordinateVector):
    @classmethod
    def dimension(cls):
        return 6


u = Vec6(1, 2, 3, 4, 5, 6)
v = Vec6(11, 12, 13, 14, 15, 16)

print(Vec6.dimension())
print(Vec6.zero())

print(repr(u + v))
print(10 * u)

print(-u)

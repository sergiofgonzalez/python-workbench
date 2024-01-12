"""
Tests that validate that equality checks for the different Vector subclasses
work as expected.
"""
import unittest

from tests.utils.testutils_coordvec import CoordVecTestUtils
from vec2 import Vec2
from vec3 import Vec3


class TestVectorDuckTyping(unittest.TestCase):
    def test_duck_typing_not_equal(self):
        u = CoordVecTestUtils.concrete_coordvec_class(dimension=2)(1, 2)
        u_1 = Vec2(1, 2)
        u_2 = Vec3(1, 2, 3)

        self.assertNotEqual(u, u_1)
        self.assertNotEqual(u, u_2)
        self.assertNotEqual(u_1, u_2)


if __name__ == "__main__":
    unittest.main()

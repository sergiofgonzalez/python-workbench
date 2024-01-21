import unittest
from creatures.model import Creature

class ValidationTest(unittest.TestCase):

    def test_invalid_type_fails(self):
        dragon = Creature(
            name="dragon",
            description=["this", "is", "supposed", "to", "be", "a", "string"],
            country="*"
        )

    def test_invalid_value_fails(self):
        dragon = Creature(
            name="dragon",
            description="d",
            country="*"
        )
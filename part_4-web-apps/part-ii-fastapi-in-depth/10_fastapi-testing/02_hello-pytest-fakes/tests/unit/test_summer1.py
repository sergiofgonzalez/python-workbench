"""First approach for testing the mod2.summer function"""

import os

os.environ["UNIT_TEST"] = "true"
from hellomock import mod2  # pylint: disable=C0413:wrong-import-position


def test_summer():
    assert "3" == mod2.summer(1, 2)

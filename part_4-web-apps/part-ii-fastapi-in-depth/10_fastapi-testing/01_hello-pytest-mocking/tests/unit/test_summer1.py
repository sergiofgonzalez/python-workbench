"""First approach for testing the mod2.summer function"""

import hellomock.mod2 as mod2


def test_summer():
    assert "The sum is 3" == mod2.summer(1, 2)

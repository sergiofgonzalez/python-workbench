"""First approach for testing the mod2.summer function"""

import pytest
from hellomock import fake_mod1
from hellomock import mod2


@pytest.fixture(name="my_obj")
def fixture_my_obj_with_fake_preamble():
    my_obj = mod2.MyClass(fake_mod1)
    return my_obj

def test_summer(my_obj):
    assert "3" == my_obj.summer(1, 2)

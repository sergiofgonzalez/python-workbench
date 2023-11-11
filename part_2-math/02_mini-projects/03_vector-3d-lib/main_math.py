"""
Sample program illustrating how to use the vec3d library API for Math
"""
from vec3d.math import (
    add
)

if __name__ == "__main__":
    v1 = (1, 1, 1)
    v2 = (2, 2, 2)
    v3 = (3, 3, 3)
    print(add(v1, v2, v3))

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

def plane_1(x, y):
    return -x - y


xs = np.linspace(-6, 6, 25)
ys = np.linspace(-6, 6, 25)

fig = plt.figure()
ax = plt.axes(projection="3d")

# x + y + z = 0
X, Y = np.meshgrid(xs, ys)
Z = plane_1(X, Y)
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap="viridis", edgecolor="none", alpha=0.6),

# x = 0
ys = np.linspace(-10, 10, 25)
zs = np.linspace(-10, 10, 25)
Y, Z = np.meshgrid(ys, zs)
X = np.zeros(Y.shape) # same as xs = yy * 0
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap="viridis", edgecolor="none", alpha=0.6),


# y = 0
xs = np.linspace(-10, 10, 25)
zs = np.linspace(-10, 10, 25)
X, Z = np.meshgrid(xs, zs)
Y = np.zeros(X.shape) # same as xs = yy * 0
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap="viridis", edgecolor="none", alpha=0.6),


ax.scatter3D(0, 0, 0, color="red")

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title("Three planes intersecting in one point")
ax.view_init(33, 33)

plt.show()
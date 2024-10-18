import matplotlib.pyplot as plt
from math import sin, pi, cos
from lines import fn_secant_line

def r(theta):
    return (-2 * 20 * 20 / -9.81) * sin(theta * pi / 180) * cos(theta * pi / 180)


fig, ax = plt.subplots()
ax.grid(True)
ax.set_xlabel(r"$ \theta °$")
ax.set_ylabel("r (m)")
ax.set_xticks(range(0, 91, 10))

ax.axhline(y=0, color="k")
ax.axvline(x=0, color="k")

ax.plot(range(0, 91), [r(theta) for theta in range(0, 91)], label=r"$ r(\theta) $")

secant_line_15 = fn_secant_line(r, 14.99, 15.01)
angles = range(5, 25)
ax.plot(angles, [secant_line_15(angle) for angle in angles], label=r"$ r(\theta) $ increasing")
ax.scatter(15, r(15))

secant_line_45 = fn_secant_line(r, 44.99, 45.01)
angles = range(30, 60)
ax.plot(angles, [secant_line_45(angle) for angle in angles], label=r"$ r(\theta) $ breaking point")
ax.scatter(45, r(45))

secant_line_75 = fn_secant_line(r, 74.99, 75.01)
angles = range(65, 85)
ax.plot(angles, [secant_line_75(angle) for angle in angles], label=r"$ r(\theta) $ decreasing")
ax.scatter(75, r(75))

ax.legend()
plt.show()
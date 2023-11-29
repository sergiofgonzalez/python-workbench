# Rendering a Octahedron using PyGame and OpenGL
> illustrates how to render the same octahedron from [05_rendering-3d-sphere](../05_rendering-3d-sphere/render_octahedron.py) but using OpenGL as the graphics backend instead of Matplotlib and PyGame to handle interactivity and other user related stuff

## Description

This example is used as a shakedown test for the OpenGL and PyGame installation. It displays a basic 3D shape (an octahedron) and allows a small set of user interactions to control how it is displayed.

### Prerequisites

You should first install the required libraries:

```bash
$ source .venv/bin/activate
$ python -m pip install -r requirements.txt
```

The OS (tested in Ubuntu 20.04.6 LTS) needs to have [FreeGLUT](https://freeglut.sourceforge.net/) installed (OpenGL Utility Toolkit):

```bash
sudo apt install freeglut3-dev
```

The examples work without GLE (GL Extrusion library), but the documentation for [PyOpenGL installation](https://pyopengl.sourceforge.net/documentation/installation.html) suggests that GLE is also needed.

In case the example is failing for you, you can install it doing:

```bash
sudo apt install libgle3-dev
```

### Usage Notes

The following user interactions have been enabled:

+ Mouse Left Button: 30° counterclockwise rotation on the z- axis.
+ Mouse Right Button: 30° counterclockwise rotation on the y- and z- axes.
+ Keypress "a": starts animation on x-, y-, and z- axes.
+ Keypress "s": stops animation.


### Known Issues

While the example works as expected, when quitting the application you get a Segmentation fault.

```
pygame 2.5.2 (SDL 2.28.2, Python 3.10.13)
Hello from the pygame community. https://www.pygame.org/contribute.html
2023-11-16 08:38:03,947 [    INFO] (vec2d.graph.vector2d_graphics) | Using vec2d.graph v0.1.1
Segmentation fault
```

This might have to do with WSL2 display driver. As it doesn't affect the program itself I havent' investigated further.
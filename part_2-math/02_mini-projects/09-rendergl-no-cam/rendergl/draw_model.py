import sys

import pygame
from matplotlib import colormaps
from OpenGL.GL import (
    GL_BACK,
    GL_COLOR_BUFFER_BIT,
    GL_CULL_FACE,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_LINES,
    GL_TRIANGLES,
    glBegin,
    glClear,
    glColor3fv,
    glCullFace,
    glEnable,
    glEnd,
    glRotatef,
    glTranslatef,
    glVertex3fv,
)
from OpenGL.GLU import gluPerspective
from pygame.locals import DOUBLEBUF, OPENGL
from vec3d.math import cross, dot, length, scale, subtract

blues_colormap = colormaps.get_cmap("Blues")


def normal(face):
    """Computes the normal vector of a triangle in 3D representing a face of
    larger 3D shape. The vertices of the triangle has to be arranged in a
    particular way so that if the triangle vertices are face[0], face[1], and
    face[2], (face[1] - face[0]) x (face[2] - face[0]) must point away from the
    shape.
    """
    return cross(subtract(face[1], face[0]), subtract(face[2], face[0]))


def unit(v):
    """Scales the given vector, so that its length is 1."""
    return scale(1.0 / length(v), v)


def shade(face, colormap=blues_colormap, light=(1, 2, 3)):
    """A Matplotlib backed, simple to understand, shading mechanism"""
    return colormap(1 - dot(unit(normal(face)), unit(light)))


def axes():
    """Draws the axes in the OpenGL canvas."""
    axes_coords = [
        [(-1000, 0, 0), (1000, 0, 0)],
        [(0, -1000, 0), (0, 1000, 0)],
        [(0, 0, -1000), (0, 0, 1000)],
    ]

    # Inform OpenGL that we're about to draw a collection of lines
    glBegin(GL_LINES)

    # Draw the azes as a series of lines
    for axis in axes_coords:
        for vertex in axis:
            # Set the color of the lines to white, with equal intensity on the
            # RGB components. In OpenGL the color intensities range from 0.0 to
            # 1.0
            glColor3fv((1, 1, 1))
            glVertex3fv(vertex)

    # Informs OpenGL that series of vertex specifications that started with
    # glBegin has ended.
    glEnd()


def draw_model(
    faces,
    *,
    colormap=blues_colormap,
    light=(1, 2, 3),
    glTranslatef_args=None,  # pylint: disable=invalid-name
    glRotatef_args=None,  # pylint: disable=invalid-name
):
    """Main function to draw a 3D shape using a PyGame window configured with an
    OpenGL backend.

    Args:
        faces (list[list[tuple[IntOrFloat, IntOrFloat, IntOrFloat]]]): a list of
           lists of triangles designating the faces of a 3D shape. Note that the
           vertices of each corresponding face must be arranged in a way that
           cross(sub(face[1], face[0]), sub(face[2], face[0])) points outwards
           from the 3D face.

        colormap: a Matplotlib colormap that will be used for shading.

        light ([tuple[IntOrFloat, IntOrFloat, IntOrFloat]): a vector giving the
            light source orientation.

        glTranslatef_args (Seq[float, float, float]): a sequence of 3 floating
            points for x, y, z that will change the perspective from which we
            observe the scene. For example, using (0.0, 0.0, -5) will move the
            scene away from the viewer 5 units; (0.0, 0.0, -25) will move it
            further, thus causing the scene to look smaller.By default,
            (0.0, 0.0, -5) will be used.

        glRotatef_args (Seq[float, float, float, float]): a sequence of 4
            floating points that will change the angle at which we observe the
            scene. The expected values are for the angle, and then specification
            about an axis given for the second, third, and fourth value. That
            is, theta, x, y, z rotates the whole scene by the angle theta about
            an axis specified by the vector (x, y, z).
    """

    # Initialize PyGame engine
    pygame.init()

    # Use a 400 x 400 pixel window
    display = (400, 400)

    # Use OpenGL backend in the PyGame window, with a built-in optimization
    # called double-buffering.
    window = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Use a 45° angle, with an aspect ratio of 1. Don't show objects closer than
    # 0.1 or further than 50 units on the z-coordinates that are rendered.
    gluPerspective(45, 1, 0.1, 50.0)

    # Observe the scene from 5 units up the z-axis (i.e. move the scene down
    # (0, 0, -5)) by default. You can also provide a different value
    if glTranslatef_args:
        glTranslatef(*glTranslatef_args)
    else:
        glTranslatef(0.0, 0.0, -5)

    if glRotatef_args:
        glRotatef(*glRotatef_args)

    # Hide polygons oriented away from the viewer
    glEnable(GL_CULL_FACE)

    # Ensure we render polygons closer to the viewer on top of those further
    # from them.
    glEnable(GL_DEPTH_TEST)

    # Hide polygons that are facing the viewer but positioned behind other
    # polygons.
    glCullFace(GL_BACK)

    clock = pygame.time.Clock()

    # We want a full rotation every 5 seconds
    degrees_per_second = 360.0 / 5.0
    degrees_per_millis = degrees_per_second / 1000.0

    # Rotation axis for the animation:
    # (0, 0, 0) means rotation disabled (default)
    rotation_axis = (0, 0, 0)

    # Translation vector that can be adjusted with the keys
    # (0, 0, 0) means no readjusting from the default (0, 0, -5)
    translation_vector = (0.0, 0.0, 0.0)

    while True:
        # Process user inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                # x, y, z handles rotation about those axes
                if event.key == pygame.K_x:
                    x, y, z = rotation_axis
                    x = 1 if x == 0 else 0
                    rotation_axis = (x, y, z)
                elif event.key == pygame.K_y:
                    x, y, z = rotation_axis
                    y = 1 if y == 0 else 0
                    rotation_axis = (x, y, z)
                elif event.key == pygame.K_z:
                    x, y, z = rotation_axis
                    z = 1 if z == 0 else 0
                    rotation_axis = (x, y, z)
                # Arrow keys and fwd/back page handles translation
                elif event.key == pygame.K_PAGEUP:
                    translation_vector = (0.0, 0.0, -0.5)
                elif event.key == pygame.K_PAGEDOWN:
                    translation_vector = (0.0, 0.0, 0.5)
                elif event.key == pygame.K_UP:
                    translation_vector = (0.0, -0.5, 0.0)
                elif event.key == pygame.K_DOWN:
                    translation_vector = (0.0, 0.5, 0.0)
                elif event.key == pygame.K_LEFT:
                    translation_vector = (-0.5, 0.0, 0.0)
                elif event.key == pygame.K_RIGHT:
                    translation_vector = (0.5, 0.0, 0.0)

        # Get elapsed millis since last frame
        milliseconds = clock.tick()

        # Check if animation is enabled
        if rotation_axis is not (0, 0, 0):
            glRotatef(degrees_per_millis * milliseconds, *rotation_axis)

        # We adjust the scene and reset for the next cycle
        if translation_vector is not (0, 0, 0):
            glTranslatef(*translation_vector)
            translation_vector = (0, 0, 0)

        # Clear both the color and depth buffer (thus initializing) the screen
        # to black
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw the axes
        axes()

        # Inform OpenGL that we're about to draw triangles
        glBegin(GL_TRIANGLES)

        # For each vertex of each face, set the color based on the shading
        # mechanism we're using.
        for face in faces:
            color = shade(face, colormap, light)
            for vertex in face:
                glColor3fv((color[0], color[1], color[2]))

                # Tell OpenGL that the current vertex is ready
                glVertex3fv(vertex)

        # Informs OpenGL that series of vertex specifications that started with
        # glBegin has ended.
        glEnd()

        # Inform PyGame that the next frame is ready, so that it can make it
        # visible
        pygame.display.flip()

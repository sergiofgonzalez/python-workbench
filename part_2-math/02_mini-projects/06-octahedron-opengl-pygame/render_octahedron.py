import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import (
    GL_BACK,
    GL_COLOR_BUFFER_BIT,
    GL_CULL_FACE,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
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
from vec3d.math import dot

from rendering import blues_colormap, normal, unit


def shade(face, colormap=blues_colormap, light=(1, 2, 3)):
    return colormap(1 - dot(unit(normal(face)), unit(light)))


octahedron = [
    [(1, 0, 0), (0, 1, 0), (0, 0, 1)],
    [(1, 0, 0), (0, 0, -1), (0, 1, 0)],
    [(1, 0, 0), (0, 0, 1), (0, -1, 0)],
    [(1, 0, 0), (0, -1, 0), (0, 0, -1)],
    [(-1, 0, 0), (0, 0, 1), (0, 1, 0)],
    [(-1, 0, 0), (0, 1, 0), (0, 0, -1)],
    [(-1, 0, 0), (0, -1, 0), (0, 0, 1)],
    [(-1, 0, 0), (0, 0, -1), (0, -1, 0)],
]

light = (1, 2, 3)

# Initialize the PyGame module
pygame.init()

# Create a surface on the screen with size 400x400, using OpenGL
display = (400, 400)
window = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set our perspective when looking at the 3D scene:
#   45 is the viewing angle
#   1 is the aspect ratio
#   0.1 and 50 put limits on the z coordinates so that objects no further than
#       50 units or closer than 0.1 will be rendered.
gluPerspective(45, 1, 0.1, 50.0)


# Observe the scene from 5 units up the z axis
# NOTE: the z axis in OpenGL are oriented with positve coordinates going down
glTranslatef(0.0, 0.0, -5)


# Hide polygons not visible from our perspective
glEnable(GL_CULL_FACE)


# Render polygons closer to us on top of those further from us
glEnable(GL_DEPTH_TEST)


# Hide polygons facings us but located behind other polygons
glCullFace(GL_BACK)


clock = pygame.time.Clock()

# We want a full rotation every 5 seconds
degrees_per_second = 360.0 / 10
degrees_per_millis = degrees_per_second / 1000
enable_animation = False

while True:
    # Process user inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] == True:
                glRotatef(30, 0, 0, 1)
            elif pygame.mouse.get_pressed()[2] == True:
                glRotatef(30, 0, 1, 1)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                enable_animation = True
            elif event.key == pygame.K_s:
                enable_animation = False

    # Wait until next frame
    milliseconds = clock.tick()

    if enable_animation:
        glRotatef(degrees_per_millis * milliseconds, 1, 1, 1)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBegin(GL_TRIANGLES)

    for face in octahedron:
        color = shade(face, blues_colormap, light)
        for vertex in face:
            glColor3fv((color[0], color[1], color[2]))
            glVertex3fv(vertex)
    glEnd()

    # Refresh on-screen display
    pygame.display.flip()

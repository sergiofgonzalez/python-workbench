"""A library that contains most of the OpenGL + PyGame boiler plate needed
to render 3D shapes.
"""
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

import camera
from transforms import polygon_map

blues_colormap = colormaps.get_cmap("Blues")


def normal(face):
    return cross(subtract(face[1], face[0]), subtract(face[2], face[0]))


def unit(v):
    return scale(1.0 / length(v), v)


def shade(face, colormap=blues_colormap, light=(1, 2, 3)):
    return colormap(1 - dot(unit(normal(face)), unit(light)))


def axes():
    axes_coords = [
        [(-1000, 0, 0), (1000, 0, 0)],
        [(0, -1000, 0), (0, 1000, 0)],
        [(0, 0, -1000), (0, 0, 1000)],
    ]
    glBegin(GL_LINES)
    for axis in axes_coords:
        for vertex in axis:
            glColor3fv((1, 1, 1))
            glVertex3fv(vertex)
    glEnd()


def draw_model(
    faces,
    colormap=blues_colormap,
    light=(1, 2, 3),
    glRotatefArgs=None,  # pylint: disable=invalid-name
    get_matrix=None,
):
    def do_matrix_transform(v):
        if get_matrix:
            raise ValueError("Matrix Transform is not supported yet")
        else:
            return v

    pygame.init()
    display = (400, 400)
    window = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    cam = camera.default_camera
    cam.set_window(window)

    gluPerspective(45, 1, 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)

    if glRotatefArgs:
        glRotatef(*glRotatefArgs)

    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glCullFace(GL_BACK)

    while cam.is_shooting():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit(0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        axes()

        glBegin(GL_TRIANGLES)

        transformed_faces = polygon_map(do_matrix_transform, faces)
        for face in transformed_faces:
            color = shade(face, colormap, light)
            for vertex in face:
                glColor3fv((color[0], color[1], color[2]))
                glVertex3fv(vertex)

        glEnd()
        cam.tick()
        pygame.display.flip()

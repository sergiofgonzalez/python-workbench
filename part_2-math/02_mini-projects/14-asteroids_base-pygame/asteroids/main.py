"""Entry point for the Asteroids game"""

import sys
from random import randint

import pygame
from vec2d.graph import Polygon, draw
from vec2d.math import translate

from asteroids.models.asteroid import Asteroid, Ship, PolygonModel

asteroid_count = 10
width, height = 400, 400

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


def to_pixels(x, y):
    return (20 * x + 200, -20 * y + 200)


def draw_poly(scr, polygon_model: PolygonModel, color=GREEN):
    screen_pixels = [to_pixels(x, y) for x, y in polygon_model.transformed()]

    # Draws multiple contiguous straight antialiased line segments
    # aalines(surface, color, closed, points, blend)
    # surface: represents the screen surface
    # color: is the color
    # closed: indicates that the lines should be closed to form a
    #   polygon
    # points: are the pixel coordinates where a line segment starts and ends
    # blend: (deprecated) if non-zero each line will be blended with the
    # surface's existing pixel shades, otherwise the pixels will be overwritten.
    pygame.draw.aalines(scr, color, True, screen_pixels)


if __name__ == "__main__":
    ship = Ship()
    asteroids = [Asteroid() for _ in range(asteroid_count)]

    for asteroid in asteroids:
        asteroid.x = randint(-9, 9)
        asteroid.y = randint(-9, 9)

    # Initialize the pygame module
    pygame.init()

    # Create a surface on screen with the given size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Asteroids")

    done = False

    while not done:
        # Get all events from pygame's event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Clear the screen
        screen.fill(BLACK)

        draw_poly(screen, ship)
        for asteroid in asteroids:
            draw_poly(screen, asteroid)

        # Update the screen
        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    sys.exit(0)

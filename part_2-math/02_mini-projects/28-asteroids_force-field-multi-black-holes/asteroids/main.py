"""Entry point for the Asteroids game"""

import sys
from math import cos, pi, sin
from random import randint

import pygame

from asteroids.models.asteroid import Asteroid, BlackHole, PolygonModel, Ship

asteroid_count = 1
width, height = 400, 400

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Can be fine-tuned to change how the ship moves
ACCELERATION = 3
SHIP_ROTATION_VELOCITY = (2 * pi) / (5 * 1000)


def to_pixels(x, y):
    return (20 * x + 200, -20 * y + 200)


def draw_poly(scr, polygon_model: PolygonModel, color=GREEN, fill=False):
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
    if fill:
        pygame.draw.polygon(scr, color, screen_pixels)
    else:
        pygame.draw.aalines(scr, color, True, screen_pixels)


def draw_segment(scr, points, color=GREEN):
    screen_pixels = [to_pixels(x, y) for x, y in points]
    pygame.draw.aaline(scr, color, screen_pixels[0], screen_pixels[1])


if __name__ == "__main__":
    ship = Ship()
    ship.x = 7
    ship.y = 3

    asteroids = [Asteroid() for _ in range(asteroid_count)]

    for asteroid in asteroids:
        asteroid.x = randint(-9, 9)
        asteroid.y = randint(-9, 9)

    # Initialize the pygame module
    pygame.init()

    # Create a surface on screen with the given size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Asteroids")

    # Create the blackhole2
    black_hole = BlackHole(0.1)
    black_hole2 = BlackHole(0.1)

    black_hole.x = 0
    black_hole.y = 0
    black_hole2.x = 5
    black_hole2.y = -5

    black_holes = [black_hole, black_hole2]

    # Used to track how fast the screen updates
    clock = pygame.time.Clock()

    done = False

    while not done:
        # get elapsed milliseconds since last frame
        milliseconds = clock.tick()

        # Get all events from pygame's event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Clear the screen
        screen.fill(BLACK)

        draw_poly(screen, ship)
        for black_hole in black_holes:
            draw_poly(screen, black_hole, fill=True)
        for asteroid in asteroids:
            asteroid.move(
                milliseconds, thrust_vector=(0, 0), gravity_sources=black_holes
            )
            draw_poly(screen, asteroid)

        # Let the black holes attract each other
        for black_hole in black_holes:
            others = [other for other in black_holes if other != black_hole]
            black_hole.move(
                milliseconds, thrust_vector=(0, 0), gravity_sources=others
            )

        # Get the state of the keyboard keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            laser_beam = ship.laser_segment()
            draw_segment(screen, laser_beam)

            for asteroid in asteroids:
                if asteroid.does_intersect(laser_beam):
                    asteroids.remove(asteroid)
            done = len(asteroids) == 0

        if keys[pygame.K_LEFT]:
            ship.rotation_angle += SHIP_ROTATION_VELOCITY * milliseconds
        if keys[pygame.K_RIGHT]:
            ship.rotation_angle -= SHIP_ROTATION_VELOCITY * milliseconds

        tx, ty = 0, 0
        if keys[pygame.K_UP]:
            tx = ACCELERATION * cos(ship.rotation_angle)
            ty = ACCELERATION * sin(ship.rotation_angle)
            # ship.vx += ax * milliseconds / 1000
            # ship.vy += ay * milliseconds / 1000
        if keys[pygame.K_DOWN]:
            tx = -ACCELERATION * cos(ship.rotation_angle)
            ty = -ACCELERATION * sin(ship.rotation_angle)

        ship.move(
            milliseconds, thrust_vector=(tx, ty), gravity_sources=black_holes
        )

        for asteroid in asteroids:
            if asteroid.does_collide(ship):
                done = True

        # Update the screen
        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    sys.exit(0)

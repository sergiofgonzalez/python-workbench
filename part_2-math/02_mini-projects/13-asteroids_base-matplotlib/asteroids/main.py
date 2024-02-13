"""Entry point for the Asteroids game"""

from random import randint

from vec2d.graph import Polygon, draw
from vec2d.math import translate

from asteroids.models.asteroid import Asteroid, Ship

if __name__ == "__main__":
    ship = Ship()
    asteroid_count = 10
    asteroids = [Asteroid() for _ in range(asteroid_count)]

    for asteroid in asteroids:
        asteroid.x = randint(-9, 9)
        asteroid.y = randint(-9, 9)

    draw(
        Polygon(*ship.points),
        *[
            Polygon(*translate((asteroid.x, asteroid.y), asteroid.points))
            for asteroid in asteroids
        ],
    )

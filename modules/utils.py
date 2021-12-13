import random
from pathlib import Path
from typing import Union

from pygame import Surface, Vector2, draw
from pygame.image import load


def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)


def create_spaceship_picture(spaceship_width, spaceship_height):
    spaceship = Surface((spaceship_width, spaceship_height))
    points = [
        (spaceship.get_width() / 2, 0),
        (spaceship.get_width() / 4, spaceship.get_height()),
        (spaceship.get_width() / 2, spaceship.get_height() * (3 / 4)),
        (spaceship.get_width() * (3 / 4), spaceship.get_height()),
        (spaceship.get_width() / 2, 0)
    ]
    draw.aalines(spaceship, (255, 255, 255), False, points, 3)

    return spaceship

"""
Drawing asteroids in surface
"""
from typing import List, Tuple

import pygame


def drawing_asteroid_in_surface(asteroid_width: int, asteroid_height: int, color: Tuple[int, int, int],
                                function_create_points) -> pygame.Surface:
    """
    Drawing asteroid on the surface

    :param asteroid_width: Asteroid width
    :param asteroid_height: Asteroid height
    :param color: Asteroid color
    :param function_create_points: Function that takes a surface and composes the location of points in this surface
    :return: Surface with asteroid
    """
    asteroid = pygame.surface.Surface((asteroid_width, asteroid_height))
    points = function_create_points(asteroid)
    pygame.draw.aalines(asteroid, color, False, points, 3)

    return asteroid


def creating_first_type_location_points_to_asteroid(asteroid: pygame.Surface) -> List[Tuple[int, int]]:
    """
    Creating the first type of location of points for an asteroid

    :param asteroid: Surface on which we want to place the points
    :return: Sequence of points
    """
    return [
        (0, asteroid.get_height() / 8),
        (asteroid.get_width() * (1 / 4), asteroid.get_height() / 2),
        (0, asteroid.get_height() * (7 / 8)),
        (asteroid.get_width() / 2, asteroid.get_height() - 1),
        (asteroid.get_width(), asteroid.get_height() * (7 / 8)),
        (asteroid.get_width() * (7 / 8), asteroid.get_height() * (5 / 8)),
        (asteroid.get_width(), asteroid.get_height() / 8),
        (asteroid.get_width() * (6 / 8), 0),
        (asteroid.get_width() / 2, asteroid.get_height() / 8),
        (asteroid.get_width() * (2 / 8), 0),
        (0, asteroid.get_height() / 8)
    ]

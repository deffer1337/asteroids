from typing import Union, Tuple

from pygame.math import Vector2

from modules.game_object import GameObject
from modules.utils import get_random_velocity
from modules.asteroids_surfaces import drawing_asteroid_in_surface, creating_first_type_location_points_to_asteroid
from modules.colors import WHITE


class Asteroid(GameObject):
    def __init__(self, position: Union[Tuple[int, int], Vector2], width: int, height: int):
        asteroid = drawing_asteroid_in_surface(width, height, WHITE, creating_first_type_location_points_to_asteroid)
        super().__init__(position, asteroid, get_random_velocity(2, 4), 4, 4)



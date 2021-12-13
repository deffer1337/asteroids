
import pygame

from modules.game_object import GameObject
from modules.utils import get_random_velocity


class Asteroid(GameObject):
    def __init__(self, position, width, height):
        asteroid = pygame.surface.Surface((width, height))
        self.points = [
            (0, asteroid.get_height() / 8),
            (asteroid.get_width() * (1/4), asteroid.get_height() / 2),
            (0, asteroid.get_height() * (7/8)),
            (asteroid.get_width() / 2, asteroid.get_height() - 1),
            (asteroid.get_width(), asteroid.get_height() * (7/8)),
            (asteroid.get_width() * (7/8), asteroid.get_height() * (5/8)),
            (asteroid.get_width(), asteroid.get_height() / 8),
            (asteroid.get_width() * (6 / 8), 0),
            (asteroid.get_width() / 2, asteroid.get_height() / 8),
            (asteroid.get_width() * (2 / 8), 0),
            (0, asteroid.get_height() / 8)
        ]
        pygame.draw.aalines(asteroid, (255, 255, 255), False, self.points, 3)
        super().__init__(position, asteroid, get_random_velocity(2, 4))


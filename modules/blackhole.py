from typing import Union, Tuple

import pygame.draw
from pygame.math import Vector2
from pygame.surface import Surface

from modules.colors import LIGHT_YELLOW


class BlackHole:
    C = 10
    G = 2.5

    def __init__(self, position: Union[Tuple[int, int], Vector2], surface: Surface, mass: Union[int, float]):
        self.position = Vector2(position)
        self.mass = mass
        self.radius = surface.get_width() / 2
        surface = surface.convert_alpha()
        pygame.draw.circle(surface, LIGHT_YELLOW, (surface.get_width() / 2, surface.get_height() / 2), self.radius,
                           width=1)
        self.sprite = surface

    def pull(self, game_object):
        v = self.position - game_object.position
        r = v.length()
        f = self.G * self.mass / (r * r)
        v = v.normalize() * f
        game_object.velocity += v

    def draw(self, surface: Surface) -> None:
        """
        Drawing game object in surface

        :param surface: The surface on which to draw the game object
        :return: None
        """
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def collides_with(self, other_game_object) -> bool:
        """
        Checking that two objects collided

        :param other_game_object: Other GameObject to check the collision
        :return: Is objects collide
        """
        distance = self.position.distance_to(other_game_object.position)
        return distance < self.radius / 6 + other_game_object.radius
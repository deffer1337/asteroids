from typing import Union, Tuple

import pygame.draw
from pygame.math import Vector2
from pygame.surface import Surface

from modules.colors import WHITE


class WhiteHole:
    C = 10
    G = 2.5

    def __init__(self, position: Union[Tuple[int, int], Vector2], surface: Surface, mass: Union[int, float]):
        self.position = Vector2(position)
        self.mass = mass
        self.radius = surface.get_width() / 2
        surface = surface.convert_alpha()
        pygame.draw.circle(surface, WHITE, (surface.get_width() / 2, surface.get_height() / 2), self.radius)
        self.sprite = surface

    def repulsion(self, game_object):
        v = self.position - game_object.position
        r = v.length()
        f = self.G * self.mass / (r * r)
        v = v.normalize() * f
        game_object.velocity -= v

    def draw(self, surface: Surface) -> None:
        """
        Drawing game object in surface

        :param surface: The surface on which to draw the game object
        :return: None
        """
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)
from abc import ABC
from typing import Tuple, Union

from pygame.math import Vector2
from pygame import Surface

from modules.utils import wrap_position


class GameObject(ABC):
    """ Base class for game object classes """

    def __init__(self, position: Union[Tuple[int, int], Vector2], sprite: Surface,
                 velocity: Union[Tuple[int, int], Vector2]):
        """
        :param position: The initial position of the game object
        :param sprite: Game object sprite
        :param velocity: Game object velocity
        """
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface: Surface) -> None:
        """
        Drawing game object in surface

        :param surface: The surface on which to draw the game object
        :return: None
        """
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface: Surface) -> None:
        """
        Move game object in surface

        :param surface: The surface on which you need to move the object
        :return: None
        """
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_game_object) -> bool:
        """
        Checking that two objects collided

        :param other_game_object: Other GameObject to check the collision
        :return: Is objects collide
        """
        distance = self.position.distance_to(other_game_object.position)
        return distance < self.radius + other_game_object.radius

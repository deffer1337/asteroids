from typing import Union, Tuple

from pygame import Surface, Vector2
from pygame import gfxdraw

from modules.game_object import GameObject
from modules.colors import WHITE


class Bullet(GameObject):
    def __init__(self, position: Union[Tuple[int, int], Vector2], velocity: Union[Tuple[int, int], Vector2],
                 bullet_width: int, bullet_height: int):
        bullet = Surface((bullet_width, bullet_height))
        gfxdraw.rectangle(bullet, (0, 0, bullet.get_width(), bullet.get_height()), (255, 255, 255))
        bullet.fill(WHITE)
        super().__init__(position, bullet, velocity)

    def move(self, surface: Surface) -> None:
        """
        Move bullet in surface

        :param surface: The surface on which you need to move the bullet
        :return: None
        """
        self.position += self.velocity

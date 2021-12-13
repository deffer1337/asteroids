from pygame import Surface
from pygame import gfxdraw

from modules.game_object import GameObject


class Bullet(GameObject):
    def __init__(self, position, velocity, bullet_width, bullet_height):
        bullet = Surface((bullet_width, bullet_height))
        gfxdraw.rectangle(bullet, (0, 0, bullet.get_width(), bullet.get_height()), (255, 255, 255))
        bullet.fill((255, 255, 255))
        super().__init__(position, bullet, velocity)

    def move(self, surface):
        self.position = self.position + self.velocity

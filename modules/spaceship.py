from typing import Union, Tuple

from pygame import Vector2, Surface
from pygame.transform import rotozoom

from modules.game_object import GameObject
from modules.bullet import Bullet
from modules.utils import create_spaceship_picture


class Spaceship(GameObject):
    MANEUVERABILITY = 5
    ACCELERATION = 0.25
    BULLET_SPEED = 15
    MAX_SPEED_X = 8
    MAX_SPEED_Y = 8

    def __init__(self, position: Union[Tuple[int, int], Vector2], spaceship_width: int, spaceship_height: int,
                 bullet_width: int, bullet_height: int, health: int, create_bullet_callback):
        """
        :param position: Spaceship starting position
        :param spaceship_width: Spaceship width
        :param spaceship_height: Spaceship height
        :param bullet_width: Spaceship bullet width
        :param bullet_height: Spaceship bullet height
        :param health: Spaceship max health
        :param create_bullet_callback: Callback for bullet
        """
        super().__init__(position,
                         create_spaceship_picture(spaceship_width, spaceship_height),
                         Vector2(0))
        self.bullet_width = bullet_width
        self.bullet_height = bullet_height
        self.direction = Vector2(0, -1)
        self.health = health
        self.create_bullet_callback = create_bullet_callback

    def rotate(self, clockwise=True) -> None:
        """
        Spaceship rotate

        :param clockwise: Clockwise
        :return: None
        """
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def velocity_limit(self, velocity: Vector2) -> Vector2:
        """
        Check spaceship velocity

        :param velocity: Spaceship velocity
        :return: Permissible velocity
        """
        if velocity.x > self.MAX_SPEED_X:
            velocity.x = self.MAX_SPEED_X
        elif velocity.x < -self.MAX_SPEED_X:
            velocity.x = -self.MAX_SPEED_X

        if velocity.y > self.MAX_SPEED_Y:
            velocity.y = self.MAX_SPEED_Y
        elif velocity.y < -self.MAX_SPEED_Y:
            velocity.y = -self.MAX_SPEED_Y

        return velocity

    def accelerate(self) -> None:
        """
        Acceleration of spaceship

        :return: None
        """
        new_velocity = self.velocity + self.direction * self.ACCELERATION
        self.velocity = self.velocity_limit(new_velocity)

    def shoot(self) -> None:
        """
        Shooting

        :return: None
        """
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity, self.bullet_width, self.bullet_height)
        self.create_bullet_callback(bullet)

    def draw(self, surface: Surface) -> None:
        """
        Drawing spaceship on surface
        :param surface:
        :return: None
        """
        angle = self.direction.angle_to(Vector2(0, -1))
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

from typing import Union, Tuple

from pygame import Vector2, Surface
from pygame.transform import rotozoom

from modules.game_object import GameObject
from modules.bullet import Bullet
from modules.utils import draw_tail_in_spaceship, create_spaceship_picture
from modules.colors import WHITE, BLACK


class Spaceship(GameObject):
    MANEUVERABILITY = 5
    ACCELERATION = 0.25
    BULLET_SPEED = 15

    def __init__(self, position: Union[Tuple[int, int], Vector2], spaceship_width: int, spaceship_height: int,
                 bullet_width: int, bullet_height: int, health: int, max_speed_x: float, max_speed_y: float,
                 create_bullet_callback):
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
                         create_spaceship_picture(spaceship_width, spaceship_height, WHITE),
                         Vector2(0), max_speed_x, max_speed_y)
        self.bullet_width = bullet_width
        self.bullet_height = bullet_height
        self.direction = Vector2(0, -1)
        self.health = health
        self.create_bullet_callback = create_bullet_callback
        self.tail = SpaceshipTail(self)

    def rotate(self, clockwise=True) -> None:
        """
        Spaceship rotate

        :param clockwise: Clockwise
        :return: None
        """
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self) -> None:
        """
        Acceleration of spaceship

        :return: None
        """
        self.velocity = self.velocity + self.direction * self.ACCELERATION

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
        :param surface: Surface on which draw the spaceship
        :return: None
        """
        angle = self.direction.angle_to(Vector2(0, -1))
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)


class SpaceshipTail:
    def __init__(self, spaceship):
        self.spaceship = spaceship

    def activate_tail(self):
        self.spaceship.sprite = draw_tail_in_spaceship(self.spaceship.sprite, WHITE)

    def deactivate_tail(self):
        self.spaceship.sprite = draw_tail_in_spaceship(self.spaceship.sprite, BLACK)

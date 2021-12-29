import random
from typing import Union, Tuple

from pygame import Surface, Vector2, draw


def wrap_position(position: Union[Tuple[int, int], Vector2], surface: Surface) -> Vector2:
    """
    :param position: Current game object position
    :param surface: Surface on which the game object lies in position
    :return: Position that does not go beyond surface
    """
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


def get_random_velocity(min_velocity: int, max_velocity: int) -> Vector2:
    """
    Get random velocity in the direction
    :param min_velocity: Min velocity
    :param max_velocity: Max velocity
    :return: Velocity
    """
    velocity = random.randint(min_velocity, max_velocity)
    angle = random.randrange(0, 360)
    return Vector2(velocity, 0).rotate(angle)


def create_spaceship_picture(spaceship_width: int, spaceship_height: int, color: Tuple[int, int, int]) -> Surface:
    """
    :param spaceship_width: Spaceship width
    :param spaceship_height: Spaceship height
    :param color: Spaceship color
    :return: Surface with spaceship picture
    """
    spaceship = Surface((spaceship_width, spaceship_height))
    points = [
        (spaceship.get_width() / 2, 0),
        (spaceship.get_width() / 4, spaceship.get_height()),
        (spaceship.get_width() / 2, spaceship.get_height() * (3 / 4)),
        (spaceship.get_width() * (3 / 4), spaceship.get_height()),
        (spaceship.get_width() / 2, 0)
    ]
    draw.aalines(spaceship, color, False, points, 3)

    return spaceship


def draw_tail_in_spaceship(spaceship: Surface, color: Tuple[int, int, int]) -> Surface:
    """
    :param spaceship: Surface spaceship
    :param color: Spaceship_tail color
    :return: Surface with spaceship_tail picture
    """
    points = [
        (spaceship.get_width() / 2, spaceship.get_height() * (3 / 4) + 4),
        (spaceship.get_width() * (3 / 4) - 4, spaceship.get_height() - 1),
        (spaceship.get_width() / 4 + 4, spaceship.get_height() - 1),
        (spaceship.get_width() / 2, spaceship.get_height() * (3 / 4) + 4)
    ]
    draw.aalines(spaceship, color, True, points)

    return spaceship


def collides_with(game_object, other_game_object) -> bool:
    """
    Checking that two objects collided

    :param game_object: GameObject to check the collision
    :param other_game_object: Other GameObject to check the collision
    :return: Is objects collide
    """
    distance = game_object.position.distance_to(other_game_object.position)
    return distance < game_object.radius + other_game_object.radius


def get_random_position_object_on_screen(screen_width, screen_height, object_width, object_height):
    return Vector2(random.randint(object_width, screen_width - object_width),
                   random.randint(object_height, screen_height - object_height))


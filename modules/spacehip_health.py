from pygame.math import Vector2

from modules.game_object import GameObject


class SpaceshipHealth(GameObject):
    """
    Game object spaceship health
    """
    def __init__(self, position, sprite):
        super().__init__(position, sprite, Vector2(0))

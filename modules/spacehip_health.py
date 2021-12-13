from modules.game_object import GameObject


class SpaceshipHealth(GameObject):
    def __init__(self, position, sprite, velocity=0):
        super().__init__(position, sprite, velocity)

import pygame
from pygame import Surface, SRCALPHA

from modules.whitehole import WhiteHole
from modules.game_object import GameObject


class TestWhiteHole:
    def setup_class(self):
        self.screen = pygame.display.set_mode((60, 60))
        self.whitehole = WhiteHole((2, 2), Surface((32, 32), SRCALPHA, 32), 1)
        self.gameobject = GameObject((40, 40), Surface((6, 6)), (0, 0), 1, 1)
        self.start_position_gameobject = self.gameobject.position

    def test_repulsion_gameobject_then_gameobject_position_far_from_white_hole(self):
        for i in range(1000):
            self.whitehole.repulsion(self.gameobject)
            self.gameobject.move(self.screen)
        assert self.gameobject.position.distance_to(self.whitehole.position) > self.gameobject.position.distance_to(
            self.start_position_gameobject)

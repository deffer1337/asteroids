import pygame
from pygame import Surface, SRCALPHA

from modules.blackhole import BlackHole
from modules.game_object import GameObject


class TestBlackHole:
    def setup_class(self):
        self.screen = pygame.display.set_mode((60, 60))
        self.blackhole = BlackHole((2, 2), Surface((32, 32), SRCALPHA, 32), 1)
        self.gameobject = GameObject((40, 40), Surface((6, 6)), (0, 0), 1, 1)
        self.start_position_gameobject = self.gameobject.position

    def test_pull_gameobject_then_gameobject_position_closer_to_blackhole(self):
        for i in range(1000):
            self.blackhole.pull(self.gameobject)
            self.gameobject.move(self.screen)
        assert self.gameobject.position.distance_to(self.blackhole.position) < self.gameobject.position.distance_to(
            self.start_position_gameobject)

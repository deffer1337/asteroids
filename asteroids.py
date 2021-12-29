import sys
import random
import time
from pathlib import Path
from typing import List
from random import randint

import pygame

from modules.spaceship import Spaceship
from modules.asteroid import Asteroid
from modules.spacehip_health import SpaceshipHealth
from modules.utils import create_spaceship_picture, get_random_position_object_on_screen
from modules.colors import BLACK, WHITE
from modules.blackhole import BlackHole
from modules.whitehole import WhiteHole
from modules.bullet import Bullet
from game_params_one import *


class Asteroids:
    """
    Сlass that initializes the game and provides the start of the game cycle
    """

    def __init__(self, width: int, height: int, asteroid_width: int, asteroid_height: int,
                 asteroid_count: int, spaceship_width: int, spaceship_height: int,
                 spaceship_health_point: int, bullet_width: int, bullet_height: int,
                 black_hole_width: int, black_hole_height: int, black_hole_mass: float,
                 white_hole_width: int, white_hole_height: int, white_hole_mass: float):
        """
        :param width: Screen width
        :param height: Screen height
        :param asteroid_width: Max asteroid width
        :param asteroid_height: Max asteroid height
        :param asteroid_count: Initial number of asteroids
        :param spaceship_width: Spaceship width
        :param spaceship_height: Spaceship height
        :param spaceship_health_point: Initial number of spaceship health
        :param bullet_width: Bullet width
        :param bullet_height: Bullet height
        """
        self._init_game()
        self.clock = pygame.time.Clock()
        self._score_for_asteroids = {(asteroid_width, asteroid_height): 50,
                                     (asteroid_width / 2, asteroid_height / 2): 100,
                                     (asteroid_width / 4, asteroid_height / 4): 200
                                     }
        self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        self.position_asteroids = ((0, 0), (self.screen.get_width(), 0), (0, self.screen.get_height()),
                                   (self.screen.get_width(), self.screen.get_height()))
        self.asteroid_max_width = asteroid_width
        self.asteroid_max_height = asteroid_height
        self.asteroid_count = asteroid_count
        self.asteroids = [Asteroid(self.position_asteroids[random.randint(0, 3)],
                                   self.asteroid_max_width,
                                   self.asteroid_max_height) for _ in range(self.asteroid_count)]
        self.bullets = []
        self.spaceship = Spaceship((self.screen.get_width() / 2, self.screen.get_height() / 2), spaceship_width,
                                   spaceship_height,
                                   bullet_width, bullet_height, spaceship_health_point, 8, 8, self.bullets.append)
        self.spaceship_healths = self._create_spaceship_health(spaceship_health_point)
        self.black_hole = None
        self.black_hole_width = black_hole_width
        self.black_hole_height = black_hole_height
        self.black_hole_mass = black_hole_mass
        self.time_to_spawn_black_hole = time.perf_counter() + randint(15, 30)
        self.time_to_delete_black_hole = time.perf_counter()
        self.white_hole = None
        self.white_hole_width = white_hole_width
        self.white_hole_height = white_hole_height
        self.white_hole_mass = white_hole_mass
        self.time_to_spawn_white_hole = time.perf_counter() + randint(15, 30)
        self.time_to_delete_white_hole = time.perf_counter()
        self.font = pygame.font.Font(Path(Path(__file__).parent, 'assets', 'Hyperspace.otf'), 30)
        self._score = 0

    def main_loop(self) -> None:
        """
        Starting the game cycle

        :return: None
        """
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _white_hole_spawn(self):
        is_white_hole_spawn = self._hole_spawn(self.white_hole,
                                               self.time_to_spawn_white_hole,
                                               self.white_hole_width,
                                               self.white_hole_height,
                                               self.white_hole_mass,
                                               WhiteHole)
        if is_white_hole_spawn:
            self.white_hole, self.time_to_delete_white_hole = is_white_hole_spawn

    def _white_hole_delete(self):
        is_white_hole_delete = self._hole_delete(self.white_hole,
                                                 self.time_to_delete_white_hole)
        if is_white_hole_delete:
            self.white_hole, self.time_to_spawn_white_hole = is_white_hole_delete

    def _black_hole_spawn(self):
        is_black_hole_spawn = self._hole_spawn(self.black_hole,
                                               self.time_to_spawn_black_hole,
                                               self.black_hole_width,
                                               self.black_hole_height,
                                               self.black_hole_mass,
                                               BlackHole)
        if is_black_hole_spawn:
            self.black_hole, self.time_to_delete_black_hole = is_black_hole_spawn

    def _black_hole_delete(self):
        is_black_hole_delete = self._hole_delete(self.black_hole,
                                                 self.time_to_delete_black_hole)
        if is_black_hole_delete:
            self.black_hole, self.time_to_spawn_black_hole = is_black_hole_delete

    def _hole_spawn(self, hole, time_to_spawn, hole_width, hole_height, hole_mass, hole_cls):
        if not hole:
            if time.perf_counter() > time_to_spawn:
                hole = hole_cls(get_random_position_object_on_screen(
                    self.screen.get_width(), self.screen.get_height(), hole_width, hole_height),
                    pygame.Surface((hole_width, hole_height), pygame.SRCALPHA, 32),
                    hole_mass
                )
                return hole, time.perf_counter() + randint(10, 15)

    def _hole_delete(self, hole, time_to_delete):
        if hole:
            if time.perf_counter() > time_to_delete:
                return None, time.perf_counter() + randint(15, 30)

    def _create_spaceship_health(self, spaceship_health_point: int) -> List[SpaceshipHealth]:
        spaceship_healths = []
        indent = 32
        for i in range(spaceship_health_point):
            spaceship_healths.append(
                SpaceshipHealth((self.screen.get_width() - indent, 32), create_spaceship_picture(32, 32, WHITE)))
            indent += 32

        return spaceship_healths

    def _init_game(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("Asteroids")

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]
        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.spaceship.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_d]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_a]:
                self.spaceship.rotate(clockwise=False)

            if is_key_pressed[pygame.K_w]:
                self.spaceship.accelerate()
                self.spaceship.tail.activate_tail()
            else:
                self.spaceship.tail.deactivate_tail()

    def _asteroid_collides_with_(self, game_object):
        if type(game_object) is not Asteroid:
            for asteroid in self.asteroids:
                if asteroid.collides_with(game_object):
                    if type(game_object) is Spaceship:
                        if self.spaceship.health > 0:
                            self.spaceship = self._get_new_spaceship()
                            self.spaceship_healths.pop()
                        else:
                            self.spaceship = None
                            break

                    if type(game_object) is Bullet:
                        self.bullets.remove(game_object)

                    for a in self._get_new_asteroids(asteroid):
                        self.asteroids.append(a)
                    self._destroy_asteroid(asteroid)
                    self._score += self._score_for_asteroids[(asteroid.sprite.get_width(),
                                                              asteroid.sprite.get_height())]
                    break

    def _get_new_spaceship(self):
        return Spaceship((self.screen.get_width() / 2, self.screen.get_height() / 2),
                         self.spaceship.sprite.get_width(),
                         self.spaceship.sprite.get_height(),
                         self.spaceship.bullet_width, self.spaceship.bullet_height,
                         self.spaceship.health - 1, 8, 8,
                         self.bullets.append)

    def _destroy_asteroid(self, asteroid):
        self.asteroids.remove(asteroid)

    def _get_new_asteroids(self, asteroid):
        if asteroid.sprite.get_width() > self.asteroid_max_width / 4 \
                and asteroid.sprite.get_height() > self.asteroid_max_height / 4:
            for a in [Asteroid(asteroid.position,
                               asteroid.sprite.get_width() / 2,
                               asteroid.sprite.get_height() / 2) for _ in range(2)]:
                yield a

    def _blackhole_collides_with(self, black_hole, game_object):
        if black_hole.collides_with(game_object):
            if type(game_object) is Asteroid:
                self._destroy_asteroid(game_object)
            if type(game_object) is Bullet:
                self.bullets.remove(game_object)
            if type(game_object) is Spaceship:
                if self.spaceship.health > 0:
                    self.spaceship = self._get_new_spaceship()
                    self.spaceship_healths.pop()
                else:
                    self.spaceship = None

    def _when_all_asteroids_destroyed(self):
        if len(self.asteroids) == 0:
            self.asteroid_count += 1
            self.asteroids = [Asteroid(self.position_asteroids[random.randint(0, 3)],
                                       self.asteroid_max_width,
                                       self.asteroid_max_height) for _ in range(self.asteroid_count)]

    def _delete_bullets_outside_screen(self):
        for bullet in self.bullets:
            if bullet.position.x < 0 or bullet.position.x > self.screen.get_width() or \
                    bullet.position.y < 0 or bullet.position.y > self.screen.get_height():
                self.bullets.remove(bullet)

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)
            if self.black_hole:
                self.black_hole.pull(game_object)
                self._blackhole_collides_with(self.black_hole, game_object)

            if self.white_hole:
                self.white_hole.repulsion(game_object)

            self._asteroid_collides_with_(game_object)

        self._when_all_asteroids_destroyed()
        self._delete_bullets_outside_screen()
        self._black_hole_spawn()
        self._black_hole_delete()
        self._white_hole_spawn()
        self._white_hole_delete()
        if not self.spaceship:
            pygame.quit()
            sys.exit()

    def _draw_score(self, screen):
        screen_text = self.font.render(f'{self._score}', True, (255, 255, 255))
        position = screen_text.get_rect(center=(80, 32))
        screen.blit(screen_text, position)

    def _draw(self):
        self.screen.fill(BLACK)
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        for spaceship_health in self.spaceship_healths:
            spaceship_health.draw(self.screen)
        self._draw_score(self.screen)
        if self.black_hole:
            self.black_hole.draw(self.screen)
        if self.white_hole:
            self.white_hole.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)


if __name__ == "__main__":
    asteroids = Asteroids(SCREEN_WIDTH, SCREEN_HEIGHT,
                          ASTEROID_WIDTH, ASTEROID_HEIGHT, ASTEROID_COUNT,
                          SPACESHIP_WIDTH, SPACESHIP_HEIGHT, SPACESHIP_HEALTH_POINT,
                          BULLET_WIDTH, BULLET_HEIGHT,
                          BLACK_HOLE_WIDTH, BLACK_HOLE_HEIGHT, BLACK_HOLE_MASS,
                          WHITE_HOLE_WIDTH, WHITE_HOLE_HEIGHT, WHITE_HOLE_MASS)
    asteroids.main_loop()

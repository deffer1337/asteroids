import sys
import random
from pathlib import Path

import pygame

from modules.spaceship import Spaceship
from modules.asteroid import Asteroid
from modules.spacehip_health import SpaceshipHealth
from modules.utils import create_spaceship_picture


class Asteroids:
    def __init__(self, width=1600, height=1200, asteroid_width=80, asteroid_height=80, asteroid_count=4,
                 spaceship_width=32, spaceship_height=32, spaceship_health_point=4, bullet_width=4, bullet_height=4):
        self._init_game()
        self._score_for_asteroids = {(asteroid_width, asteroid_height): 50,
                                     (asteroid_width / 2, asteroid_height / 2): 100,
                                     (asteroid_width / 4, asteroid_height / 4): 200
                                     }
        self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        self.position_asteroids = ((0, 0), (self.screen.get_width(), 0), (0, self.screen.get_height()),
                                   (self.screen.get_width(), self.screen.get_height()))
        self.clock = pygame.time.Clock()
        self.asteroid_max_width = asteroid_width
        self.asteroid_max_height = asteroid_height
        self.asteroid_count = asteroid_count
        self.asteroids = [Asteroid(self.position_asteroids[random.randint(0, 3)],
                                   self.asteroid_max_width,
                                   self.asteroid_max_height) for _ in range(self.asteroid_count)]
        self.bullets = []
        self.spaceship = Spaceship((self.screen.get_width() / 2, self.screen.get_height() / 2), spaceship_width,
                                   spaceship_height,
                                   bullet_width, bullet_height, spaceship_health_point, self.bullets.append)
        self.spaceship_healths = self._create_spaceship_health(spaceship_health_point)
        self.font = pygame.font.Font(Path(Path(__file__).parent, 'assets', 'Hyperspace.otf'), 30)
        self._score = 0

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _create_spaceship_health(self, spaceship_health_point):
        spaceship_healths = []
        indent = 32
        for i in range(spaceship_health_point):
            spaceship_healths.append(
                SpaceshipHealth((self.screen.get_width() - indent, 32), create_spaceship_picture(32, 32)))
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

    def _asteroid_collides_with_spaceship(self):
        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    if self.spaceship.health > 0:
                        self.spaceship = Spaceship((self.screen.get_width() / 2, self.screen.get_height() / 2),
                                                   self.spaceship.sprite.get_width(),
                                                   self.spaceship.sprite.get_height(),
                                                   self.spaceship.bullet_width, self.spaceship.bullet_height,
                                                   self.spaceship.health - 1,
                                                   self.bullets.append)
                        for a in self._get_new_asteroids(asteroid):
                            self.asteroids.append(a)
                        self._destroy_asteroid(asteroid)
                        self._score += self._score_for_asteroids[(asteroid.sprite.get_width(),
                                                                  asteroid.sprite.get_height())]
                        self.spaceship_healths.pop()
                    else:
                        self.spaceship = None
                        break

    def _destroy_asteroid(self, asteroid):
        self.asteroids.remove(asteroid)

    def _get_new_asteroids(self, asteroid):
        if asteroid.sprite.get_width() > self.asteroid_max_width / 4 \
                and asteroid.sprite.get_height() > self.asteroid_max_height / 4:
            for a in [Asteroid(asteroid.position,
                               asteroid.sprite.get_width() / 2,
                               asteroid.sprite.get_height() / 2) for _ in range(2)]:
                yield a

    def _asteroids_collides_with_bullet(self):
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if asteroid.collides_with(bullet):
                    for a in self._get_new_asteroids(asteroid):
                        self.asteroids.append(a)
                    self._destroy_asteroid(asteroid)
                    self._score += self._score_for_asteroids[(asteroid.sprite.get_width(),
                                                              asteroid.sprite.get_height())]
                    self.bullets.remove(bullet)
                    break

    def _when_all_asteroids_destroyed(self):
        if len(self.asteroids) == 0:
            self.asteroid_count += 1
            self.asteroids = [Asteroid(self.position_asteroids[random.randint(0, 3)],
                                       self.asteroid_max_width,
                                       self.asteroid_max_height) for _ in range(self.asteroid_count)]

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        self._asteroids_collides_with_bullet()
        self._when_all_asteroids_destroyed()
        self._asteroid_collides_with_spaceship()
        if not self.spaceship:
            pygame.quit()
            sys.exit()

    def _draw_score(self, screen):
        screen_text = self.font.render(f'{self._score}', True, (255, 255, 255))
        position = screen_text.get_rect(center=(80, 32))
        screen.blit(screen_text, position)

    def _draw(self):
        self.screen.fill((0, 0, 0))
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        for spaceship_health in self.spaceship_healths:
            spaceship_health.draw(self.screen)
        self._draw_score(self.screen)
        pygame.display.flip()
        self.clock.tick(60)


if __name__ == "__main__":
    asteroids = Asteroids()
    asteroids.main_loop()

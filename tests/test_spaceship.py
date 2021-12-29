from modules.spaceship import Spaceship


class TestSpaceship:
    def setup_class(self):
        self.bullets = []
        self.spaceship = Spaceship((0, 0), 32, 32, 2, 2, 4, 8, 8, self.bullets.append)

    def test_shoot_when_one_shoot_then_len_bullets_one(self):
        self.spaceship.shoot()
        assert len(self.bullets) == 1

    def test_accelerate_when_accelerate_then_velocity_not_start_velocity(self):
        self.spaceship.accelerate()
        assert self.spaceship.velocity == (self.spaceship.direction * self.spaceship.ACCELERATION)

    def test_rotate_when_clockwise_true_then_spaceship_turns_to_right(self):
        self.spaceship.rotate(True)
        assert self.spaceship.direction.x > 0

    def test_rotate_when_clockwise_false_then_spaceship_turns_to_left(self):
        self.spaceship.rotate(False)
        assert self.spaceship.direction.x < 0



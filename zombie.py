""" Zombie and Zombie_Handler classes. """
import time
import random
import math
import rect
import character


class Zombie_Handler:
    """ Runs all the zombie stuff so the main game just has to run update and shot for this. """
    def __init__(self):
        self.zombies = []
        self.time_until_spawn = 0

    def spawn(self, main):
        """ Spawn a zombie every now and again. How often depends on score.
        If lots of spawn time has gone by spawn lots of zombies. """
        spawn_num = int(-self.time_until_spawn)
        self.time_until_spawn -= main.dtime
        spawn_time = 2 / (main.game.score / 50 + 1)
        for _ in range(spawn_num):
            self.zombies.append(Zombie(main))
            self.time_until_spawn += spawn_time

    def update(self, main):
        """ Update the zombies, spawn them. """
        self.spawn(main)
        self.validate(main)
        for zombie in self.zombies:
            zombie.update(main)

    def show(self, main):
        """ Show all the zombies. """
        for zombie in self.zombies:
            zombie.show(main)
            
    def validate(self, main):
        """ Forget about all the dead zombies. """
        zombies = []
        for zombie in self.zombies:
            if zombie.health > 0:
                zombies.append(zombie)
        main.game.score += len(self.zombies) - len(zombies)
        self.zombies = zombies


class Zombie(character.Character):
    """ Cool as zombie class.
    Speed and health depend on player score. """
    def __init__(self, main):
        self.rotation = 0
        self.radius = 0.015
        self.velocity = min(0.1 + main.game.score / 1000, 3)
        self.set_pos()
        self.alive = True
        self.spawn_time = time.time()
        self.running_time = 0
        self.damage = 10
        self.hit_cool_down = 0  # How much longer until the zombie can hit the player?
        self.max_health = 24 * (1 + main.game.score / 5)
        self.health = self.max_health

    def set_pos(self):
        """ Choose a spawn point for the zombie. """
        pos = rect.Pos(random.random(), random.choice([-self.radius, 1 + self.radius]))
        # pos = rect.Pos(0.5, 0.5)
        if random.choice([True, False]):
            self.pos = rect.Pos(pos.y, pos.x)
        else:
            self.pos = pos

    def move(self, main):
        """ Point the zombie in the right direction (Towards the player) and move it a little.
        The zombie will stop moving if the distance from the zombie to the player is 0.75 of the
        sum of the radii. """
        self.rotation = math.atan2(main.game.player.pos.y - self.pos.y,
                                   main.game.player.pos.x - self.pos.x)
        distance = self.pos.distance(main.game.player)
        if distance >= (self.radius + main.game.player.radius) * 0.75:
            self.pos.y += math.sin(self.rotation) * self.velocity * main.dtime
            self.pos.x += math.cos(self.rotation) * self.velocity * main.dtime

    def update(self, main):
        """ Move, rotate """
        self.move(main)
        self.hit_cool_down = max(0, self.hit_cool_down - main.dtime)
        self.running_time += main.dtime

    def show(self, main):
        """ Show the zombie. """
        image_number = (7 * self.running_time) % len(main.images["zombie"])
        image = main.images["zombie"][str(int(image_number))]
        # self.show_hit_circle(main, (255, 0, 0))
        self.show_shadow(main)
        self.show_image(image, main)
        self.show_health_bar(main)
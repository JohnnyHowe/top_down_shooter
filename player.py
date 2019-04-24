""" Player object - child of character object. """
# pylint: disable=no-member
import math
import time
import pygame
import rect
from weapons import pistol
from character import Character


class Player(Character):
    """ Player object - child of character object. """
    def __init__(self):
        Character.__init__(self)
        self.pos = rect.Pos(0.5, 0.5)  # Multiplied by screen width.
        self.radius = 0.02  # Multiplied by screen width.
        self.velocity = 0.15  # Screen widths per second.
        self.running_time = None
        self.hand_offset = rect.Pos(0.6, 0.41)  # Multiplied by the radius.
        self.gun = pistol.Pistol()
        self.max_health = 100
        self.health = self.max_health

    def take_damage(self, main):
        """ Is the player hit? If so, take damage. """
        for zombie in main.game.zombie_handler.zombies:
            distance = math.sqrt((self.pos.x - zombie.pos.x) ** 2 + (self.pos.y - zombie.pos.y) ** 2)
            if distance < self.radius + zombie.radius:
                if zombie.hit_cool_down == 0:
                    self.health -= zombie.damage
                    zombie.hit_cool_down += 0.2

    def move(self, main):
        """ Move the character based on WASD input. """
        keys = pygame.key.get_pressed()
        movement = rect.Pos(0, 0)
        if keys[pygame.K_w]:
            movement.y -= 1
        if keys[pygame.K_s]:
            movement.y += 1
        if keys[pygame.K_a]:
            movement.x -= 1
        if keys[pygame.K_d]:
            movement.x += 1
        self.last_movement = movement
        multiplier = 1 - abs(0.29289 * int(movement.x and movement.y))
        self.pos.x += movement.x * main.dtime * self.velocity * multiplier
        self.pos.y += movement.y * main.dtime * self.velocity * multiplier

    def shoot(self, main):
        """ If the mouse is clicked, run self.gun.shoot. """
        for event in main.pygame_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.gun.shoot(main)

    def update_run_timer(self):
        """ If the player isn't moving, set self.running_time to None.
        If they are moving, set self.running_time to zero (if not already set). """
        if self.last_movement.x or self.last_movement.y:
            if self.running_time is None:
                self.running_time = 0
        else:
            self.running_time = None

    def hand_pos(self):
        """ Get the unscaled coordinates of the players hand - an anchor for the gun. """
        hand_pos = self.pos.copy()
        hand_pos.x += self.hand_offset.x * self.radius
        hand_pos.y += self.hand_offset.y * self.radius
        hand_pos.rotate_around(self.pos, self.rotation)
        return hand_pos

    def update(self, main):
        """ Update the player - move, rotate, update image timer """
        self.move(main)
        self.keep_on_screen()
        self.rotate(main)
        self.update_run_timer()
        self.shoot(main)
        self.take_damage(main)
        self.gun.update(main)
        if self.running_time is not None:
            self.running_time += main.dtime

    def rotate(self, main):
        """ Set self.rotation to the angle between (east,) the player and the mouse. """
        mouse_pos = main.game.mouse_pos(main)
        mouse_pos.scale_up(1 / main.game_window_width, 1 / main.game_window_width)
        self.rotation = math.atan2(mouse_pos.y - self.pos.y, mouse_pos.x - self.pos.x)

    def choose_image(self, main):
        """ Choose the correct image. """
        if self.running_time is not None:
            image_time = 0.1
            run_time = self.running_time
            num_images = len(main.images["player"]["run"])
            image_num = int((run_time % (image_time * num_images)) / image_time)
            return main.images["player"]["run"][str(image_num)]
        return main.images["player"]["still"]

    def show(self, main):
        """ Show the player hit circle (green) and the "still" image. """
        # self.show_hit_circle(main)
        self.show_shadow(main)
        self.show_image(self.choose_image(main), main)
        self.gun.show(main)
        self.show_health_bar(main)

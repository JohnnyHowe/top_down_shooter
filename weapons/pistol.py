""" Contains Pistol and Pistol_Shot classes. """
import math
import pygame
import rect
import time


class Pistol:
    """ Semi auto, 1 damage. """
    def __init__(self):
        self.width = 0.11  # Multiplied by the player radius
        self.clip_size = 8
        self.clip = self.clip_size
        self.reload_time = 0.8  # second
        self.reloading = 0

    def show(self, main):
        """ Show the gun. """
        image = main.images["guns"]["pistol"]["pistol"]
        image_size = rect.Size(pygame_rect=image.get_rect())

        scale = (2 * self.width * main.game_window_width * main.game.player.radius) / image_size.h
        image_size.w *= scale
        image_size.h *= scale

        scaled_image = pygame.transform.scale(image, image_size.get_rounded_values())
        rotated_image = pygame.transform.rotate(scaled_image, -math.degrees(main.game.player.rotation))

        hand_pos = main.game.player.hand_pos()
        hand_pos.scale_up(main.game_window_width, main.game_window_width)
        rotated_size = rect.Size(pygame_rect=rotated_image.get_rect())
        image_pos = rect.Pos(hand_pos.x - rotated_size.w / 2, hand_pos.y - rotated_size.h / 2)

        main.game_window.blit(rotated_image, image_pos.get_rounded_values())

    def reload(self, main):
        """ If the clip is empty or r is pressed, reload the clip. """
        manual_reload = main.is_tapped(pygame.K_r) and self.clip_size != self.clip
        auto_reload = self.clip == 0
        if (manual_reload or auto_reload) and not self.reloading:
            self.reloading = self.reload_time
            self.clip = self.clip_size
        self.reloading = max(0, self.reloading - main.dtime)

    def update(self, main):
        """ Update function, called every frame. """
        self.reload(main)

    def shoot(self, main):
        """ Add a shot to main.shot_handler. """
        if self.clip > 0 and not self.reloading:
            main.game.shot_handler.add_shot(Pistol_Shot(main))
            self.clip -= 1


class Pistol_Shot:
    """ Does damage over one frame in a straight line to one zombie only.
    Displayed for a fraction of a second. """
    def __init__(self, main):
        self.point1 = main.game.player.hand_pos()
        self.set_point2(main)
        self.spawn_time = time.time()
        self.show_time = 0.05
        self.done_damage = False
        self.damage = 30
        self.zombie = self.find_hit_zombie(main)
        if self.zombie:
            self.reset_point2(main)

    def set_point2(self, main):
        """ Set self.point2 - just another point on the path the bullet would travel. """
        dx = math.sin(main.game.player.rotation)
        dy = math.cos(main.game.player.rotation)
        multiplier = 1.4
        self.point2 = rect.Pos(self.point1.x + dy * multiplier, self.point1.y + dx * multiplier)

    def reset_point2(self, main):
        """ If a zombie is hit, make the pistol shot end at that zombie. """
        dx = math.sin(main.game.player.rotation)
        dy = math.cos(main.game.player.rotation)
        distance = math.sqrt((self.point1.x - self.zombie.pos.x) ** 2 +
                                (self.point1.y - self.zombie.pos.y) ** 2)
        multiplier = distance / (dx ** 2 + dy ** 2)
        self.point2 = rect.Pos(self.point1.x + dy * multiplier, self.point1.y + dx * multiplier)

    def deal_damage(self, main):
        """ Deal damage, if a zombie is hit. """
        if self.zombie:
            self.zombie.health -= self.damage
            self.done_damage = True

    def find_hit_zombie(self, main):
        """ return the zombie hit by the shot.
        uses min distance from point to line math.
        Formula is found on https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line """
        dx = self.point2.x - self.point1.x
        dy = self.point2.y - self.point1.y

        zombies = []
        for zombie in main.game.zombie_handler.zombies:
            dest_point = zombie.pos.copy()

            dp = self.point2.x * self.point1.y - self.point2.y * self.point1.x
            top = dy * dest_point.x - dx * dest_point.y + dp
            bottom = math.sqrt(dy ** 2 + dx ** 2)
            distance = abs(top) / bottom

            mouse_pos = main.game.mouse_pos(main, scale_down=True)
            mouse_angle = math.atan2(mouse_pos.y - main.game.player.pos.y, mouse_pos.x - main.game.player.pos.x)
            zombie_angle = math.atan2(zombie.pos.y - main.game.player.pos.y, zombie.pos.x - main.game.player.pos.x)
            d_angle = abs(mouse_angle - zombie_angle)

            player_dist = math.sqrt((main.game.player.pos.x - zombie.pos.x) ** 2 +
                                 (main.game.player.pos.y - zombie.pos.y) ** 2)

            if distance <= zombie.radius and d_angle <= math.pi / 2:
                zombies.append((zombie, player_dist))

        if zombies:
            zombies.sort(key=lambda x: x[1])
            return zombies[0][0]

    def update(self, main):
        """ Update the show - just do damage. """
        if not self.done_damage:
            self.deal_damage(main)

    def show(self, main):
        """ Show the shot - A line from the player in the direction of the shot.
        Shot is displayed even after the damage is done. """
        pos1 = self.point1.scale_for_window(main)
        pos2 = self.point2.scale_for_window(main)
        pygame.draw.line(main.game_window, (0, 0, 0), pos1, pos2)

    def is_valid(self):
        """ Return false after a second of this shot existing. """
        if time.time() - self.spawn_time <= self.show_time:
            return True
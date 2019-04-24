""" Base character object - only to be used as a parent class. """
import pygame
import math
import rect


class Character:
    """ Base character object - only to be used as a parent class. """
    def __init__(self):
        self.radius = 0.05
        self.pos = rect.Pos(0.5, 0.5)
        self.rotation = 0
        self.max_health = 10
        self.health = self.max_health

    def show_hit_circle(self, main, color=(0, 255, 0)):
        """ Show the hit circle - just a circle at self.pos with self.radius. """
        pos = self.pos.scale_for_window(main)
        pygame.draw.circle(main.game_window, color, pos, int(self.radius * main.game_window_width))

    def show_image(self, image, main):
        """ Show the image but scale and rotate it correctly.
        The image is scaled so the mean of the dimentions is self.radius.
        The image is rotated to self.rotation.
        Placed on self.pos. """
        image_size = rect.Size(pygame_rect=image.get_rect())
        avg_side = image_size.w + image_size.h
        scale = (self.radius / avg_side) * main.game_window_width * 4
        image_size.scale_up(w_scale=scale, h_scale=scale)
        scaled_image = pygame.transform.scale(image, image_size.get_rounded_values())
        rotated_image = pygame.transform.rotate(scaled_image, -math.degrees(self.rotation))
        rotated_rect = rect.Size(pygame_rect=rotated_image.get_rect())
        pos = self.pos.copy()
        pos.scale_up(x_scale=main.game_window_width, y_scale=main.game_window_width)
        pos.x -= rotated_rect.w / 2
        pos.y -= rotated_rect.h / 2
        main.game_window.blit(rotated_image, pos.get_rounded_values())

    def keep_on_screen(self):
        """ Make sure the player does not go off the screen - set boundaries on the position. """
        self.pos.x = max(min(1 - self.radius, self.pos.x), self.radius)
        self.pos.y = max(min(1 - self.radius, self.pos.y), self.radius)

    def show_shadow(self, main):
        """ Show a black circle. """
        pos = self.pos.scale_for_window(main)
        radius = int(self.radius * main.game_window_width * 0.8)
        shadow_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surf, (0, 0, 0, 100), (radius, radius), radius)
        main.game_window.blit(shadow_surf, (pos[0] - radius, pos[1] - radius))

    def show_health_bar(self, main):
        """ Show a little health bar above the characters head.
        Gets values from self.max_health and self.health. """
        bar_width = self.radius * 2
        bar_height = bar_width * 0.2
        health_per = max(self.health, 0) / self.max_health
        bar_pos = rect.Pos(self.pos.x - bar_width / 2, self.pos.y - self.radius - bar_height * 2)
        bar_pos = bar_pos.scale_for_window(main)
        bar_width *= main.game_window_width
        bar_height *= main.game_window_width
        pygame.draw.rect(main.game_window, (200, 0, 0), (bar_pos[0], bar_pos[1], bar_width, bar_height))
        pygame.draw.rect(main.game_window, (0, 200, 0), (bar_pos[0], bar_pos[1], bar_width * health_per, bar_height))

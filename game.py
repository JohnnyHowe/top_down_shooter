""" Game object, controls all the game things. """
import pygame
import player
import shot_handler
import zombie
import rect


class Game:
    """ Main game object, contains all the updating and showing functions. """
    def __init__(self):
        """ Initialize all the objects: Player, Zombie (and handler),
        Lock the input to the game. """
        self.player = None
        self.shot_handler = None
        self.reset_objects()
        pygame.event.set_grab(True)
        self.pause = False
        self.score_font = None

    def reset_objects(self):
        """ (Re)set all the objects used in the game: the Player, Zombie (and handler) """
        self.player = player.Player()
        self.shot_handler = shot_handler.Shot_Handler()
        self.zombie_handler = zombie.Zombie_Handler()
        self.score = 0

    def update_frame(self, main):
        """ Update everything. """
        self.player.update(main)
        self.shot_handler.update(main)
        self.zombie_handler.update(main)

        if self.player.health <= 0:
            self.reset_objects()

    def update_game(self, main):
        """ Run the game. """
        if not self.pause:
            self.update_frame(main)
            if main.is_tapped(pygame.K_ESCAPE):
                self.pause = True
                pygame.event.set_grab(False)
        else:
            pygame.event.set_grab(False)
            if main.is_tapped(pygame.K_ESCAPE):
                self.pause = False
                pygame.event.set_grab(True)

    def show_score(self, main):
        """ Show the score (zombies killed) in the top right. """
        if not self.score_font:
            self.update_score_font(main)
        text_surf = self.score_font.render("Score: {}".format(self.score * 10), True, (0, 0, 0))
        margin = main.game_window_width // 50
        main.full_window.blit(text_surf, (margin, margin))

    def show_clip(self, main):
        """ Show a bar in the top right of the screen, representing bullets in the gun. """
        bar_height = main.game_window_width // 20
        bar_width = bar_height * 5
        clip_per = max(self.player.gun.clip, 0) / self.player.gun.clip_size
        bar_pos = rect.Pos(main.full_window_size.w - bar_width - bar_height * (2/5), bar_height * (2/5))
        if self.player.gun.reloading:
            bar_fill = bar_width - bar_width * (self.player.gun.reloading / self.player.gun.reload_time)
        else:
            bar_fill = bar_width * clip_per
        pygame.draw.rect(main.full_window, (0, 0, 0),
                         (bar_pos.x, bar_pos.y, bar_width, bar_height))
        pygame.draw.rect(main.full_window, (150, 150, 150),
                         (bar_pos.x, bar_pos.y, round(bar_fill), bar_height))

    def update_score_font(self, main):
        """ Called when window size changes.
        Updates the font (size) for the score counter. """
        size = main.game_window_width // 20
        self.score_font = pygame.font.SysFont('Courier New', size)

    def update_display(self, main):
        """ Completely update the display - Clear the screen, show items, update window. """
        # background = pygame.transform.scale(main.images["background"], (main.game_window_width,) * 2)
        # main.game_window.blit(background, (0, 0))
        main.game_window.fill((202, 200, 200))
        self.shot_handler.show(main)
        self.player.show(main)
        self.zombie_handler.show(main)

    def pause_func(self, main):
        """ Called when escape is pressed. """
        window_size = main.full_window_size.get_values()
        background = pygame.Surface(window_size)
        pygame.draw.rect(background, (255, 255, 255), (0, 0, window_size[0], window_size[1]))
        background.set_alpha(128)
        main.full_window.blit(background, (0, 0))

    def mouse_pos(self, main, scale_down=False):
        """ Get the mouse position on the game window. """
        mouse_pos_tup = pygame.mouse.get_pos()
        mouse_pos = rect.Pos(mouse_pos_tup[0], mouse_pos_tup[1])
        mouse_pos.x -= main.game_window_offset.x
        mouse_pos.y -= main.game_window_offset.y
        if scale_down:
            mouse_pos.x /= main.game_window_width
            mouse_pos.y /= main.game_window_width
        return mouse_pos

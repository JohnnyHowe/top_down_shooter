""" The main program file.
This game is made primarily with objects. """
# pylint: disable=no-member
import pygame
import glob
import game
import rect


class Main:
    """ Main object - contains pygame window, clock """
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-function-args
    # This will contains lots of isntance variables - but that's okay, I swear.

    def __init__(self):
        self.full_window = None
        self.full_window_size = None
        self.game_window = None
        self.game_window_width = None
        self.set_window()

        self.clock = pygame.time.Clock()
        self.dtime = 0

        self.pygame_events = []
        self.images = image_dict("images")

        self.game = game.Game()

    def set_window(self, size=rect.Size(800, 600)):
        """ Set self.window to a new window of dimentions size (and self.full_window_rect)
        Set self.game_window to a square surface to be centred on the main window. """
        self.full_window = pygame.display.set_mode(
            size.get_values(), pygame.RESIZABLE)
        self.full_window_size = size
        self.game_window_width = min([size.w, size.h])
        self.game_window = pygame.Surface((self.game_window_width,) * 2)
        self.game_window_offset = rect.Pos(x=(self.full_window_size.w-self.game_window_width)/2,
                                           y=(self.full_window_size.h-self.game_window_width)/2)

    def event_loop(self):
        """ Run the pygame event loop and quit when the quit button and escape are pressed.
        Set self.pygame_events to the pygame events.
        Set self.dtime to the time since this was last called in seconds. """
        self.pygame_events = pygame.event.get()
        self.dtime = self.clock.tick() / 1000
        for event in self.pygame_events:
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_ESCAPE:
            #         pygame.quit()
            #         quit()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def is_tapped(self, button):
        """ Has the button been tapped?
        (Is it in the pygame events thing?) """
        for event in main.pygame_events:
            if event.type == pygame.KEYDOWN:
                if event.key == button:
                    return True

    def update_window(self):
        """ Update self.window if the window has been resized. """
        for event in self.pygame_events:
            if event.type == pygame.VIDEORESIZE:
                self.set_window(size=rect.Size(event.w, event.h))
                self.game.update_score_font(self)

    def run(self):
        """ Run the program.
        Currently skips into game. """
        while True:
            self.run_game()

    def run_game(self):
        """ Run one frame of the game. """
        self.event_loop()
        self.update_window()
        self.game.update_game(main)
        self.game.update_display(main)
        self.display_game()

    def display_game(self):
        """ Run all the display functions for the game and
        blit the game_window to the main_window. """
        self.full_window.fill((100, 100, 100))
        self.full_window.blit(self.game_window, self.game_window_offset.get_rounded_values())
        self.game.show_score(self)
        self.game.show_clip(self)
        if self.game.pause:
            self.game.pause_func(self)
        pygame.display.update()


def image_dict(folder):
    """ Return a dictionary of the images in folder, with sub-folders as sub-dicts. """
    images = {}
    items = glob.glob(folder + "/*")
    for path in items:
        if path.lower().endswith(".png"):
            images[file_name(path)] = pygame.image.load(path)
        else:
            images[file_name(path)] = image_dict(path)
    return images


def file_name(path):
    """ Return the name of the folder or item without the full path. """
    for index in range(len(path) - 1, -1, -1):
        if path[index] == "\\":
            index += 1
            break
    name = path[index:]
    if name.endswith(".png"):
        name = name[:-4]
    return name


if __name__ == "__main__":
    pygame.init()
    main = Main()
    main.run()

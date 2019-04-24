""" An object to handle all the shots/bullets.
Will call update and show methods for all shots. """


class Shot_Handler:
    """ Handles all the shots. Shots must have an update and show method. """
    def __init__(self):
        self.shots = []

    def add_shot(self, shot):
        """ add shot to self.shots.
        shot will already be an object. """
        self.shots.append(shot)

    def update(self, main):
        """ Update and validate all the shots. """
        self.validate_shots()
        for shot in self.shots:
            shot.update(main)

    def show(self, main):
        """ Show all the shots - just run shot.show(main) for all shots. """
        for shot in self.shots:
            shot.show(main)

    def validate_shots(self):
        """ Ensure all shots are "valid".
        delete shots that don't return True from shot.is_valid. """
        valid = []
        for shot in self.shots:
            if shot.is_valid():
                valid.append(shot)
        self.shots = valid
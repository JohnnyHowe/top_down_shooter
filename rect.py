""" Contains Rect, Size and Pos classes with extra helper functions. """
import math


class Rect:
    """ Class to manage rect objects
    Contains values x, y, w, h. If a value is not needed it is left as None. """
    def __init__(self, x=None, y=None, w=None, h=None, pygame_rect=None):
        """ x, y, w, h are all integers.
        pygame_rect is a pygame rect object. If not none, the values will be derived from this. """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        if pygame_rect is not None:
            self.from_pygame_rect(pygame_rect)

    def touching(self, other_rect):
        """ Is self and the other_rect touching? """
        return (self.x + self.w >= other_rect.x and
                self.x <= other_rect.x + other_rect.w and
                self.y + self.h >= other_rect.y and
                self.y <= other_rect.y + other_rect.h)

    def get_rounded_values(self):
        """ get_values function, but rounded. """
        values = self.get_values()
        return list([round(value) for value in values])

    def get_values(self):
        """ Return all values (x, y, w, h) (in tuple) regardless of type. """
        return self.x, self.y, self.w, self.h

    def scale_up(self, x_scale=1, y_scale=1, w_scale=1, h_scale=1):
        """ Scale the items up (if they exist).
        x.., y.., w.. and h_scale are all numbers (int or float).
        new is a bool, if this is true, a copy of self is scaled and returned, rather than
            modifying the current object and not returning anything. """
        if self.x is not None:
            self.x *= x_scale
        if self.y is not None:
            self.y *= y_scale
        if self.w is not None:
            self.w *= w_scale
        if self.h is not None:
            self.h *= h_scale

    def from_pygame_rect(self, rect):
        """ Get the info from the pygame rect object. """
        self.x = rect.x
        self.y = rect.y
        self.w = rect.width
        self.h = rect.height

    def copy(self):
        """ Return a copy of self. """
        return Rect(self.x, self.y, self.w, self.h)

    def __str__(self):
        """ return string in format "Rect(x, y, w, h)". """
        return "Rect({})".format(self.get_values())

    def __repr__(self):
        """ Just return __str__ result. """
        return self.__str__()


class Pos(Rect):
    """ Same as rect but only x and y.
    A few different functions. """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = None
        self.h = None

    def rotate_around(self, point, angle):
        """ Rotate self around point with angle degrees. """
        qx = point.x + math.cos(angle) * (self.x - point.x) - math.sin(angle) * (self.y - point.y)
        qy = point.y + math.sin(angle) * (self.x - point.x) + math.cos(angle) * (self.y - point.y)
        self.x = qx
        self.y = qy

    def distance(self, other):
        """ What's the distance from self to other?. """
        return math.sqrt((self.x - other.pos.x) ** 2 + (self.y - other.pos.y) ** 2)

    def touching(self, other_rect):
        """ Currently just a placeholder to disable the Rect version of this function. """
        raise TypeError("""FINISH THE "touching" METHOD OF THE Pos CLASS NOW!""")
        
    def from_pygame_rect(self, rect):
        """ Just disabling the rect version """
        raise TypeError("Cannot get pos from pygame rect")

    def copy(self):
        """ Just copy self. """
        return Pos(self.x, self.y)

    def get_values(self):
        """ Return a tuple of x and y. """
        return self.x, self.y

    def scale_for_window(self, main):
        """ Returned a tuple of the rounded, scaled values. """
        return round(self.x * main.game_window_width), round(self.y * main.game_window_width)


class Size(Rect):
    """ Same as rect but only x and y.
    A few different functions. """
    def __init__(self, w=None, h=None, pygame_rect=None):
        self.x = None
        self.y = None
        self.w = w
        self.h = h
        if pygame_rect:
            self.from_pygame_rect(pygame_rect)

    def touching(self, other_rect):
        """ Currently just a placeholder to disable the Rect version of this function. """
        raise TypeError("""FINISH THE "touching" METHOD OF THE Size CLASS NOW!""")
        
    def from_pygame_rect(self, rect):
        """ Just disabling the rect version """
        self.w = rect.width
        self.h = rect.height

    def copy(self):
        """ Just copy self. """
        return Pos(self.w, self.h)

    def get_values(self):
        """ Return a tuple of x and y. """
        return self.w, self.h

    def scale_for_window(self, main):
        """ Returned a tuple of the rounded, scaled values. """
        return round(self.w * main.game_window_width), round(self.h * main.game_window_width)


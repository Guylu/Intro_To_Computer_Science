import math

from basics import BaseObject
from torpedo import Torpedo, SpecialTorpedo

RADIUS = 1
ROTATE = 7
START_LIFE = 3
SHOOTING_FACTOR = 2


class Ship(BaseObject):
    def __init__(self, x, x_speed, y, y_speed, deg):
        super(Ship, self).__init__(x, x_speed, y, y_speed, deg, RADIUS)
        self.__life = START_LIFE

    def __add_deg(self, deg):
        """
        add required degrees to rotate ship
        :param deg: amount of degrees to add
        :return: None
        """
        self.set_deg(self.get_deg() + deg)

    def rotate_right(self):
        """
        self explanatory :P
        :return: None
        """
        self.__add_deg(-ROTATE)

    def rotate_left(self):
        """
        self explanatory :P
        :return: None
        """
        self.__add_deg(ROTATE)

    def shoot(self, is_special):
        """
        generate a new shot based on ship's attributes
        :param is_special: if True generate a special shot which follows an asteroid
        :return: generated shot
        """
        x, y = self.get_location()
        old_x_speed, old_y_speed = self.get_speed()
        deg = self.get_deg()

        new_x_speed = old_x_speed + SHOOTING_FACTOR * math.cos(
            math.radians(deg))
        new_y_speed = old_y_speed + SHOOTING_FACTOR * math.sin(
            math.radians(deg))

        return Torpedo(x, new_x_speed, y, new_y_speed, deg) if not is_special \
            else \
            SpecialTorpedo(x, new_x_speed, y, new_y_speed, deg)

    def accelerate(self):
        """
        increase ship's speed in required direction
        :return: None
        """
        x_spped, y_speed = self.get_speed()

        new_x_speed = x_spped + math.cos(math.radians(self.get_deg()))
        new_y_speed = y_speed + math.sin(math.radians(self.get_deg()))

        self.set_speed(new_x_speed, new_y_speed)

    def man_down(self):
        """
        reduce one life
        :return: None
        """
        self.__life += -1

    def man_count(self):
        """
        :return: remaining life
        """
        return self.__life

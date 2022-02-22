import math

from basics import BaseObject

RADIUS = 4
BASE_TTL = 200
SPECIAL_TTL = 600
RAD_OF_90_DEG = math.pi / 2
SPEED_CAP = 8


class Torpedo(BaseObject):
    def __init__(self, x, x_speed, y, y_speed, deg):
        super(Torpedo, self).__init__(x, x_speed, y, y_speed, deg, RADIUS)
        self.__ttl = BASE_TTL

    def reduce(self):
        """
        reduce the time to live of the torpedo by 1
        the torpedo will be removed once it's ttl is 0
        :return: the new ttl
        """
        self.__ttl -= 1
        return self.__ttl

    def set_ttl(self, ttl):
        """
        self explanatory :P
        :param ttl: the new ttl
        :return: None
        """
        self.__ttl = ttl


class SpecialTorpedo(Torpedo):
    ASTEROID_VAR = 'asteroid_location'
    SPEED_FACTOR = 2

    def __init__(self, x, x_speed, y, y_speed, deg):
        super().__init__(x, x_speed * self.SPEED_FACTOR, y, y_speed *
                         self.SPEED_FACTOR, deg)
        self.set_ttl(SPECIAL_TTL)

    @staticmethod
    def __get_sign(value):
        """
        returns the sign factor as 1 or -1
        :param value: a number to determine it's sign
        :return: sign factor
        """
        return 1 if value > 0 else -1

    def recalibrate(self, asteroid_x, asteroid_y):
        """
        calculate the direction in which torpedo should move based on asteroid location
        :param asteroid_x:
        :param asteroid_y:
        :return: None
        """
        x_speed, y_speed = self.get_speed()
        x, y = self.get_location()

        new_speed_x = x_speed + asteroid_x - x
        speed_x_sign = SpecialTorpedo.__get_sign(new_speed_x)

        new_speed_y = y_speed + asteroid_y - y
        speed_y_sign = SpecialTorpedo.__get_sign(new_speed_y)

        denominator = RAD_OF_90_DEG if asteroid_x - x == 0 else asteroid_x - x
        self.set_deg(
            math.degrees(math.atan((asteroid_y - y) / denominator)))

        self.set_speed(
            ((new_speed_x * speed_x_sign) % SPEED_CAP) * speed_x_sign,
            ((new_speed_y * speed_y_sign) % SPEED_CAP) * speed_y_sign)

    def move(self, world_max, world_min, **kwargs):
        """
        special shot's move also recalculates it's movement
        :param world_max: pair of max x,y coordinates, used for regular movement
        :param world_min: pair of min x,y coordinates, used for regular movement
        :param kwargs: contains the location of the asteroid to follow
        :return: None
        """
        if self.ASTEROID_VAR in kwargs:
            self.recalibrate(*kwargs[self.ASTEROID_VAR])

        super(SpecialTorpedo, self).move(world_max, world_min)

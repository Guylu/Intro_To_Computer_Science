import math

RADIUS = 4


class Torpedo:
    def __init__(self, x, x_speed, y, y_speed, deg):
        self.__x = x
        self.__x_speed = x_speed
        self.__y = y
        self.__y_speed = y_speed
        self.__deg = deg
        self.__ttl = 200

    def get_location(self):
        return self.__x, self.__y

    def set_location(self, x, y):
        self.__x = x
        self.__y = y

    def get_speed(self):
        return self.__x_speed, self.__y_speed

    def set_speed(self, x_speed, y_speed):
        self.__x_speed = x_speed
        self.__y_speed = y_speed

    def get_deg(self):
        return self.__deg

    def get_radius(self):
        return RADIUS

    def reduce(self):
        self.__ttl -= 1
        return self.__ttl


class SpecialTorpedo(Torpedo):
    def __init__(self, x, x_speed, y, y_speed, deg):
        super().__init__(x, x_speed, y, y_speed, deg)
        self.__ttl = 10000

    def recalibrate(self, asteroid_x, asteroid_y):
        x, y = self.get_location()
        x_delta = asteroid_x - x
        y_delta = asteroid_y - y

        self.__deg = math.atan(y_delta / x_delta)

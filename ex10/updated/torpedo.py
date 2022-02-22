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

    def set_deg(self, deg):
        self.__deg = deg

    def get_radius(self):
        return RADIUS

    def reduce(self):
        self.__ttl -= 1
        return self.__ttl

    def set_ttl(self, ttl):
        self.__ttl = ttl


class SpecialTorpedo(Torpedo):
    def __init__(self, x, x_speed, y, y_speed, deg):
        super().__init__(x, x_speed * 2, y, y_speed * 2, deg)
        self.set_ttl(100000000)

    def recalibrate(self, asteroid_x, asteroid_y, asteroid_x_speed, asteroid_y_speed):
        x_speed, y_speed = self.get_speed()
        x, y = self.get_location()

        new_speed_x = x_speed + asteroid_x - x
        new_speed_y = y_speed + asteroid_y - y
        speed_x_sign = 1 if new_speed_x > 0 else -1
        speed_y_sign = 1 if new_speed_y > 0 else -1

        self.set_speed(((new_speed_x * speed_x_sign) % 10) * speed_x_sign,
                       ((new_speed_y * speed_y_sign) % 10) * speed_y_sign)

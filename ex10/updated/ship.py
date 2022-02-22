RADIUS = 1


class Ship:
    def __init__(self, x, x_speed, y, y_speed, deg):
        self.__x = x
        self.__x_speed = x_speed
        self.__y = y
        self.__y_speed = y_speed
        self.__deg = deg
        self.__life = 3

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

    def add_deg(self, deg):
        self.__deg += deg

    def get_radius(self):
        return 1

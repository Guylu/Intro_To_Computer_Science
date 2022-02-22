import math


class Asteroid:
    def __init__(self, x, x_speed, y, y_speed, size):
        self.__x = x
        self.__x_speed = x_speed
        self.__y = y
        self.__y_speed = y_speed
        self.__size = size

    def get_size(self):
        return self.__size

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

    def get_radius(self):
        return self.get_size() * 10 - 5

    def has_intersection(self, obj):
        distance = math.sqrt(
            (obj.get_location()[0] - self.get_location()[0]) ** 2 +
            (obj.get_location()[1] - self.get_location()[1]) ** 2)

        return distance <= obj.get_radius() + self.get_radius()

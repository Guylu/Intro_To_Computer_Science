import math

from basics import BaseObject

SIZE_FACTOR = 10
SIZE_PADDING = 5
TWO_D_FACTOR = 2


class Asteroid(BaseObject):
    def __init__(self, x, x_speed, y, y_speed, size):
        super(Asteroid, self).__init__(
            x, x_speed, y, y_speed, radius=Asteroid.calculate_radius(size),
            deg=None)
        self.__size = size

    @staticmethod
    def calculate_radius(size):
        """
        asteroid's radius is derived from it's size, therfore the calculation
        :param size: asteroid's size
        :return: calculated radius
        """
        return size * SIZE_FACTOR - SIZE_PADDING

    def get_size(self):
        """
        self explanatory :P
        :return:
        """
        return self.__size

    def has_intersection(self, other):
        """
        check if asteroid has an intersection with the object given by other
        :param other: an object within screen derived from BasicObject
        :return: True if collides False otherwise
        """
        my_x, my_y = self.get_location()
        other_x, other_y = other.get_location()
        distance = math.sqrt(
            (other_x - my_x) ** TWO_D_FACTOR + (other_y - my_y) ** TWO_D_FACTOR)

        return distance <= other.get_radius() + self.get_radius()

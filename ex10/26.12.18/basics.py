class BaseObject:
    """
    a base class for all objects that will appear within screen.
    as all these objects have the functionality here in common,
    we reduce duplication by using inheritance.
    """

    def __init__(self, x, x_speed, y, y_speed, deg, radius):
        self.__x = x
        self.__x_speed = x_speed
        self.__y = y
        self.__y_speed = y_speed
        self.__deg = deg
        self.__radius = radius

    def set_location(self, x, y):
        self.__x = x
        self.__y = y

    def get_location(self):
        return self.__x, self.__y

    def set_speed(self, x_speed, y_speed):
        self.__x_speed = x_speed
        self.__y_speed = y_speed

    def get_speed(self):
        return self.__x_speed, self.__y_speed

    def set_deg(self, deg):
        self.__deg = deg

    def get_deg(self):
        return self.__deg

    def get_radius(self):
        return self.__radius

    def move(self, world_max, world_min, **kwargs):
        """
        set the new location for object based on it's speed and direction
        :param world_max: pair of max x,y coordinates, used to overlap screen
        :param world_min: pair of min x,y coordinates, used to overlap screen
        :param kwargs: used for parameters that adds functionality in sub-classes
        :return: None
        """
        max_x, max_y = world_max
        min_x, min_y = world_min

        self.__x = (self.__x_speed + self.__x - min_x) % (max_x - min_x) + min_x
        self.__y = (self.__y_speed + self.__y - min_y) % (max_y - min_y) + min_y

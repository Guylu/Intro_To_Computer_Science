class Car:
    """
    this class will handle the car objects in the board - all their movement
    etc...
    """
    __ROW = 0
    __COLUMN = 1
    __INC = 1
    __NON = 0
    __HORIZONTAL = 1
    __VERTICAL = 0
    __START = 0
    __END = -1
    __UP = "u"
    __DOWN = "d"
    __RIGHT = "r"
    __LEFT = "l"
    __DES_UP = "will go 1 move up"
    __DES_DOWN = "will go 1 move down"
    __DES_RIGHT = "will go 1 move right"
    __DES_LEFT = "will go 1 move left"

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col)
         location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # initialize values:
        self.__name = name
        self.__length = length
        self.__location = list(location)
        self.__orientation = orientation

    def get_orientation(self):
        """
        :return: car orientation
        """
        return self.__orientation

    def get_location(self):
        """
        :return: cars location
        """
        return self.__location

    def get_length(self):
        """
        :return: cars length
        """
        return self.__length

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        # dynamically sort coordinates:
        coordinates_list = []
        # delta_h - horizontal delta
        # delta_p - vertical delta
        delta_h = self.__INC
        delta_p = self.__NON
        if self.__orientation == self.__HORIZONTAL:
            delta_h = self.__NON
            delta_p = self.__INC

        for i in range(self.__length):
            coordinates_list.append((self.__location[self.__ROW] + delta_h * i,
                                     self.__location[self.__COLUMN]
                                     + delta_p * i))
        return coordinates_list

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements
        permitted by this car.
        """
        if self.__orientation == self.__VERTICAL:
            return {self.__UP: self.__DES_UP,
                    self.__DOWN: self.__DES_DOWN}
        else:
            return {self.__RIGHT: self.__DES_RIGHT,
                    self.__LEFT: self.__DES_LEFT}

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for
        this move to be legal.
        """
        if self.__orientation == self.__VERTICAL:  # vertical
            if movekey == self.__UP:
                return [(self.car_coordinates()[self.__START][self.__ROW] - 1,
                         self.car_coordinates()[self.__START][self.__COLUMN])]

            else:  # down
                return [(self.car_coordinates()[self.__END][self.__ROW] + 1,
                         self.car_coordinates()[self.__END][self.__COLUMN])]

        else:  # HORIZONTAL
            if movekey == self.__RIGHT:
                return [(self.car_coordinates()[self.__END][self.__ROW],
                         self.car_coordinates()[self.__END][self.__COLUMN] + 1)]

            else:  # "left"
                return [(self.car_coordinates()[self.__START][self.__ROW],
                         self.car_coordinates()[self.__START][
                             self.__COLUMN] - 1)]

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if movekey not in self.possible_moves():
            return False

        if movekey == self.__UP:
            self.__location[self.__ROW] -= 1

        elif movekey == self.__DOWN:
            self.__location[self.__ROW] += 1

        elif movekey == self.__LEFT:
            self.__location[self.__COLUMN] -= 1

        elif movekey == self.__RIGHT:
            self.__location[self.__COLUMN] += 1

        return True

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name

class Board:
    """
    this class will handle the board of the game - will set all the objects
    in it and will handle movement of cats etc..
    """
    __ROW = 0
    __COLUMN = 1
    __INC = 1
    __NON = 0
    __SIZE_BOARD = 7
    __HORIZONTAL = 1
    __VERTICAL = 0
    __START = 0
    __END = -1
    __UP = "u"
    __DOWN = "d"
    __RIGHT = "r"
    __LEFT = "l"
    __NO_CAR = "no such car in board, choose again"
    __NOT_DIRECTION = "not valid direction"
    __EMPTY = "_ "
    __SPACE = " "
    __EMPTY_STR = ""
    __NEW_LINE = "\n"
    __TARGET = (3, 7)
    __WINNING = 2
    __CAR_LENGTH = 0
    __CAR_POSITION = 1
    __CAR_ORIENTATION = 2
    __INFO_POSITION = 1
    __LOCATION = 0

    def __init__(self):
        """
        creates the board
        """
        self.__board = [[self.__NON] * self.__SIZE_BOARD,
                        [self.__NON] * self.__SIZE_BOARD,
                        [self.__NON] * self.__SIZE_BOARD,
                        [self.__NON] * self.__SIZE_BOARD,
                        [self.__NON] * self.__SIZE_BOARD,
                        [self.__NON] * self.__SIZE_BOARD,
                        [self.__NON] * self.__SIZE_BOARD]
        self.__wining_place = self.__NON

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        # The game may assume this function returns a reasonable
        # representation of the board for printing, but may not assume
        # details about it.
        return_str = self.__EMPTY_STR
        for i in range(len(self.__board)):
            for j in range(len(self.__board[self.__ROW])):
                if self.__board[i][j] == self.__NON:
                    return_str += self.__EMPTY  # print regular "_" empty cell
                else:
                    return_str += self.__board[i][j].get_name() + self.__SPACE
                    # here print the name of the car

            return_str += self.__NEW_LINE

        return return_str

    def get_length(self):
        """
        :return: lengths of board
        """
        # both row and column length:
        return len(self.__board), len(self.__board[self.__ROW])

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        # In this board, returns a list containing the cells in the square
        # from (0,0) to (6,6) and the target cell (3,7)
        # all coordinates in the board:
        list_of_coordinates = []
        for i in range(len(self.__board)):
            for j in range(len(self.__board[self.__ROW])):
                list_of_coordinates.append((i, j))
        # plus the target:
        list_of_coordinates.append(self.target_location())
        return list_of_coordinates

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        list_possible_moves = []
        for i in range(len(self.__board)):
            for j in range(len(self.__board[self.__ROW])):
                # if not empty - there's car
                if self.__board[i][j] != self.__NON:
                    temp_car = self.__board[i][j]
                    # for every car found, run this function:
                    self.possible_moves_helper(temp_car, list_possible_moves)

        return list_possible_moves

    def possible_moves_helper(self, car, list_possible_moves):
        """
        this function will update list_possible_moves to have the correct
        information
        :param car: car object
        :param list_possible_moves: list of all possible moves
        :return:
        """
        # if the car has already been checked, return:
        if self.already_there(list_possible_moves, car.get_name()):
            return
        # dict info from car will assist:
        possible = enumerate(car.possible_moves())
        for move in possible:
            # if move is valid:
            if self.check_move(car, move[self.__INFO_POSITION]):
                # if valid then add it with the form (name,movekey,description)
                list_possible_moves.append((car.get_name(),
                                            move[self.__INFO_POSITION],
                                            car.possible_moves()
                                            [move[self.__INFO_POSITION]]))

    def already_there(self, list_moves, name):
        """
        checks if the name of he car is already in the list list_moves
        :param list_moves: list of valid moves
        :param name: name of car
        :return: true if found, false otherwise
        """
        for l in list_moves:
            for item in l:
                if name in item:
                    return True
        return False

    def target_location(self):
        """
        This function returns the coordinates of the location which is to
        be filled for victory.
        :return: (row,col) of goal location
        """
        # In this board, returns (3,7)
        return self.__TARGET

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        # special check for target:
        if coordinate == self.target_location():
            if self.__wining_place == self.__NON:
                return None
            else:
                return self.__wining_place
        #  checks the coordinates if on board they point to empty spot:
        result = self.__board[coordinate[self.__ROW]][coordinate[self.__COLUMN]]
        if result == self.__NON:
            return None
        # if we got here then it is not empty - its a car - we can checks its
        #  name:
        return result.get_name()

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Remember to consider all the reasons adding a car can fail.
        # You may assume the car is a legal car object following the API.
        # implement your code and erase the "pass"
        # checks if certain values are valid:
        car_length = len(car.car_coordinates())
        car_location = car.car_coordinates()[0]
        if not self.check_values([car_length, car_location,
                                  car.get_orientation()]):
            # if found "bad" values - return False
            return False
        # checks to see all the coordinates we want to place the car in are
        # empty on the board:
        for coordinates in car.car_coordinates():
            if self.__board[coordinates[self.__ROW]][coordinates[self.__COLUMN]] \
                    != self.__NON:
                return False

        # check if car with this name already exists:
        if self.find_car(car.get_name()) != (None, None):
            return False

        # finally all good!!
        # place the car:
        for coordinates in car.car_coordinates():
            self.__board[coordinates[self.__ROW]][
                coordinates[self.__COLUMN]] = car

        return True

    def check_values(self, key):
        """
        checks if certain values in the jason file are valid
        :param key: representation of content of jason file - list
        :return: if the checks have gone though successfully - true\ false
        """

        board_length = self.get_length()
        # length check::
        # vertical check:
        if (key[self.__CAR_ORIENTATION] == self.__VERTICAL and key[
            self.__CAR_LENGTH]
                not in range(board_length[self.__ROW])):
            return False
        # horizontal check:
        elif key[self.__CAR_ORIENTATION] == self.__HORIZONTAL and \
                key[self.__CAR_LENGTH] not in \
                range(board_length[self.__COLUMN]):
            return False
        # coordinates check:
        row = key[self.__CAR_POSITION][self.__ROW]
        column = key[self.__CAR_POSITION][self.__COLUMN]
        # row should be inside the board:
        if row not in range(board_length[self.__ROW]):
            return False
        # column should be inside the board:
        if column not in range(board_length[self.__COLUMN]):
            return False
        # if we got here then all is good!
        return True

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        # finds the location of car by name:
        i, j = self.find_car(name)
        if i is None:
            print(self.__NO_CAR)
            return False
        temp_car = self.__board[i][j]
        # checks wining:
        if self.game_won(temp_car, movekey):
            return self.__WINNING
        # checks if the movement on the board is legal:
        if self.check_move(temp_car, movekey):
            # moves car:
            temp_car.move(movekey)
            # moves car in board:
            self.move_coordinates(temp_car, i, j, movekey)
            return True
        # not valid movement:
        print(self.__NOT_DIRECTION)
        return False

    def game_won(self, car, movekey):
        """
        checks if the game has been won
        :param car: car object
        :param movekey: the direction of movement
        :return: True is won, False otherwise
        """
        won = tuple((self.target_location()[self.__ROW],
                     self.target_location()[self.__COLUMN] - 1))

        if car.car_coordinates()[self.__END] == won and \
                movekey == self.__RIGHT:
            self.__wining_place = car.get_name()
            return True

        return False

    def move_coordinates(self, car, i, j, movekey):
        """
        moves car coordinates on the board
        :param car: car object
        :param i: x coordinate of car
        :param j: y coordinate of car
        :param movekey: the direction of movement
        :return:
        """
        # moves the coordinates according to the movekey:
        if movekey == self.__UP:
            self.__board[i + car.get_length() - 1][j] = self.__NON
            self.__board[i - 1][j] = car

        elif movekey == self.__DOWN:
            self.__board[i + car.get_length()][j] = car
            self.__board[i][j] = self.__NON

        elif movekey == self.__LEFT:
            self.__board[i][j + car.get_length() - 1] = self.__NON
            self.__board[i][j - 1] = car

        elif movekey == self.__RIGHT:
            self.__board[i][j + car.get_length()] = car
            self.__board[i][j] = self.__NON

    def find_car(self, name):
        """
        will find the location on the board of a given cars name
        :param name: name of car to look for
        :return: coordinates of the car
        """
        for i in range(len(self.__board)):
            for j in range(len(self.__board[self.__ROW])):
                if self.__board[i][j] != self.__NON and \
                        self.__board[i][j].get_name() == name:
                    return i, j
        return None, None

    def check_move(self, car, movekey):
        """
        checks if the movement on the board is legal
        :param car: car object
        :param movekey: the direction of movement
        :return:whether it is legal - true \ false
        """
        # uses the cars method:
        movement = car.movement_requirements(movekey)[self.__LOCATION]
        # movement should be in the board:
        if movement not in self.cell_list():
            return False
        # or on the target location
        if movement == self.target_location():
            return True
        # movement should be towards an empty sport of the board
        if self.__board[movement[self.__ROW]][
            movement[self.__COLUMN]] != self.__NON:
            return False
        # all checks went though!
        return True

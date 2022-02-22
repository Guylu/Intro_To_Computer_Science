import os
import sys
import helper
import car
import board

BAD_PATH = "invalid file path!"
VALID_NAMES = ["Y", "B", "O", "G", "W", "R"]
VALUES = 1
CAR_LENGTH = 0
CAR_POSITION = 1
CAR_ORIENTATION = 2
MIN_CAR = 2
MAX_CAR = 5


class Game:
    """
    this class handles all the functions of the game  - has all the logic
    """
    __WINNING = 2
    __VALID_MOVES = ["u", "d", "l", "r"]
    __HORIZONTAL = 1
    __VERTICAL = 0
    __ROWS = 0
    __COLUMN = 1
    __CHOOSE_INPUT = "choose a car from the board, and a direction:"
    __NOT_DIRECTION = "not valid direction"
    __GAME_WON_MSG = "congrats! won!"
    __CAR = 0
    __DIRECTION = 2

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.__board = board

    def __single_turn(self):
        """
        runs a single instance of the game - one turn
        """
        # users input:
        user_input = input(self.__CHOOSE_INPUT)

        # should choose only cars from the board:
        car_chosen = user_input[self.__CAR]

        # should only choose valid directions
        direction = user_input[self.__DIRECTION]
        if direction not in self.__VALID_MOVES:
            print(self.__NOT_DIRECTION)
            return
        # try to move car:
        run = self.__board.move_car(car_chosen, direction)
        if not run:
            return

        # here means all is good!!

        # check for game winning:
        if run == self.__WINNING:
            return True

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        # implement your code here (and then delete the next line - 'pass')
        while True:
            # play while not won:
            print(self.__board)
            if self.__single_turn():
                print(self.__GAME_WON_MSG)
                return


def load_game():
    game_board = board.Board()

    # jason file read:
    jason_file = sys.argv[VALUES]
    # if not os.path.isfile(jason_file):
    #     print(BAD_PATH)
    #     return  # if bad file return
    # implement jason data:
    jason_dic = helper.load_json(jason_file)
    for item, key in jason_dic.items():
        # only valid names of cars:
        if item not in VALID_NAMES:
            continue
        # only valid lengths of cars:
        if key[CAR_LENGTH] not in range(MIN_CAR, MAX_CAR):
            continue
        # car creation!
        temp_car = car.Car(item, key[CAR_LENGTH],
                           key[CAR_POSITION],
                           key[CAR_ORIENTATION])
        # try to add to board:
        if not game_board.add_car(temp_car):
            continue

    return game_board


if __name__ == "__main__":
    # Your code here
    # All access to files, non API constructors, and such must be in this
    # section, or in functions called from this section.
    game = Game(load_game())
    game.play()

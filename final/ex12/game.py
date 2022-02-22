class Game:
    """
    this class will handle the entire logic of the game 4 in a row
    """
    EMPTY = 0
    SEQ_LENGTH = 4
    __COLUMNS = 7
    __ROWS = 6
    __PLAYERS = 2

    def __init__(self):
        """
        initialize a clean game
        """
        self.board = Game.get_empty_board()
        self.__turn = self.EMPTY
        self.__game_status = None

    @staticmethod
    def get_empty_board():
        """
        creates empty board
        :return:
        """
        return [[Game.EMPTY] * Game.__COLUMNS for i in range(Game.__ROWS)]

    @staticmethod
    def get_cols():
        """
        :return: num of columns in board
        """
        return Game.__COLUMNS

    @staticmethod
    def get_rows():
        """
        :return: num of rows in board
        """
        return Game.__ROWS

    def __get_seq(self, row, col, player, row_step=0, col_step=0):
        """
        calculates the sequence of pegs the player has generated per direction
        :param row: row of peg
        :param col: col of peg
        :param player: num of player
        :param row_step: whether to go in row direction - and where: left/right)
        :param col_step: whether to go in col direction - and where: up/down)
        :return:the seq that is generated - list of tuples
        """
        try:
            if self.get_player_at(row, col) != player:
                return []
        except KeyError:
            return []

        seq = [(row, col)]

        if col_step < 0 or (col_step == 0 and row_step < 0):
            seq = self.__get_seq(
                row + row_step, col + col_step, player, row_step, col_step) + seq
        else:
            seq += self.__get_seq(
                row + row_step, col + col_step, player, row_step, col_step)

        return seq

    def created_sequences(self, row, col, player):
        """
        calculate the sequence a player ( or AI :) ) move generates
        :param row: row of move
        :param col: col of move
        :param player: player num of the player that made the move
        :return: list of sequences ordered by size
        """
        if player != self.get_player_at(row, col):
            return []

        sequences = list()

        sequences.append(self.__get_seq(row, col - 1, player, col_step=-1) +
                         self.__get_seq(row, col, player, col_step=1))

        sequences.append(self.__get_seq(row, col, player, row_step=1))

        sequences.append(
            self.__get_seq(row - 1, col - 1, player, row_step=-1, col_step=-1) +
            self.__get_seq(row, col, player, row_step=1, col_step=1))

        sequences.append(
            self.__get_seq(row, col, player, row_step=1, col_step=-1) +
            self.__get_seq(row - 1, col + 1, player, row_step=-1, col_step=1))

        sequences.sort(key=lambda seq: len(seq), reverse=True)

        return sequences

    def end_game(self, row, col):
        """
        check if game is over for any given reason
        :param row: last move row
        :param col: last move col
        :return:
        """
        player = self.get_current_player()

        # check if current player won
        sequences = self.created_sequences(row, col, player)
        if len(sequences[0]) >= self.SEQ_LENGTH:
            self.__game_status = player
            return sequences[0]

        # check tie
        if row == 0:
            for cell in self.board[row]:
                if cell == self.EMPTY:
                    return
            self.__game_status = 0

    def get_free_row(self, column):
        """
        check for the lowest empty row in a given column, raise exception if there's none
        :param column: col in the game board
        :return: the free row in the column
        """
        illegal_move = "Illegal move."
        if self.__game_status is not None:
            raise KeyError(illegal_move)

        free_row = -1
        for row in range(self.__ROWS):
            if self.get_player_at(row, column) is not None:
                break

            free_row = row

        if free_row == -1:
            raise KeyError(illegal_move)

        return free_row

    def make_move(self, column):
        """
        make a move in the game - a move is made by setting the highest free row
        in a given to the value of current player (according to game turns count)
        :param column: chosen col to make a move in
        :return: row of the cell that was changed
        """
        player = self.get_current_player()

        row = self.get_free_row(column)

        self.board[row][column] = player

        self.end_game(row, column)

        self.__turn += 1

        return row

    def get_winner(self):
        """
        :return: the player who won!
        """
        return self.__game_status

    def get_player_at(self, row, col):
        """
        calculate the num of player in given position, None represents a free sell
        :param row: row in board
        :param col: col in board
        :return: return the player num or None
        """
        if row < self.EMPTY or row >= self.__ROWS or \
                col < self.EMPTY or col >= self.__COLUMNS:
            raise KeyError("Illegal location.")

        if self.board[row][col] == self.EMPTY:
            return None

        return self.board[row][col]

    def get_current_player(self):
        """
        calculate the num of player based on turn count
        :return: player num
        """
        return self.__turn % self.__PLAYERS + 1

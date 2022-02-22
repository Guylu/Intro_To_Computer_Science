import random

from .game import Game


class GameSimulator(Game):
    """
    a helping class for ai that handles stripped game logic matched for ai needs
    """

    def __init__(self, master_game, player):
        """
        initialize the copy of the game
        :param master_game: the game state given to the AI
        :param player: num of player representing the current turn
        """
        super().__init__()
        self.board = GameSimulator.__get_board_copy(master_game)
        self.player = player

    @staticmethod
    def __get_board_copy(master_game):
        """
        create a duplicate board for the ai
        :param master_game: the game state given to the AI
        :return: copied board
        """
        board = Game.get_empty_board()
        for col in range(Game.get_cols()):
            for row in range(Game.get_rows() - 1, -1, -1):
                value = master_game.get_player_at(row, col)
                if value is None:
                    break
                board[row][col] = value

        return board

    def get_current_player(self):
        """
        override base game functionality in order to bypass the turn mechanism
        :return: the current player turn within the simulation
        """
        return self.player

    def end_game(self, row, col):
        """
        override base game functionality which is not required for ai usage
        """
        pass

    def set_player(self, player):
        """
        set the current player in order to bypass the turn mechanism
        :param player:
        :return:
        """
        self.player = player


class AI:
    """
    AI class: alexa, what is the next move?
    """
    __SCORES = {0: 0, 1: 1, 2: 10, 3: 50}
    __MAX_SCORE = 100
    __GAME_OVER_FACTOR = -20
    __SEQ_FACTOR = 10

    def __init__(self, game, player):
        self.__game = game
        self.__player = player
        self.__mid = Game.get_cols() // 2
        self.__last_found_move = 0

    def __best_sequence(self, sequences, simulator):
        """
        get the score of each created sequence and return the one with the highest score
        when calculating scores consider the possibility to continue the sequence
        :param sequences:
        :param simulator:
        :return:
        """
        if len(sequences[0]) >= Game.SEQ_LENGTH:
            return self.__MAX_SCORE, len(sequences[0])

        best_score = 0
        seq_len = 0

        for sequence in sequences:
            curr_score = self.__SCORES.get(len(sequence), self.__MAX_SCORE)

            row_step = max(-1, min(1, sequence[-1][0] - sequence[0][0]))
            col_step = max(-1, min(1, sequence[-1][1] - sequence[0][1]))

            if row_step == 0 and col_step == 0:
                break

            try:
                if simulator.get_player_at(
                        sequence[-1][0] + row_step,
                        sequence[-1][1] + col_step) is not None:
                    curr_score = curr_score / self.__SEQ_FACTOR
            except KeyError:
                curr_score = curr_score / self.__SEQ_FACTOR

            try:
                if simulator.get_player_at(
                        sequence[0][0] - row_step,
                        sequence[0][1] - col_step) is not None:
                    curr_score = curr_score / self.__SEQ_FACTOR
            except KeyError:
                curr_score = curr_score / self.__SEQ_FACTOR

            if curr_score > best_score:
                best_score = curr_score
                seq_len = len(sequence)

        return best_score, seq_len

    def __get_location_value(self, player, other_player, depth, game, col):
        """
        evaluate a given move value for a player.
        evaluation is made based on the max sequence created by the move,
        minus the best calculated move for the opponent calculated with recursion.
        :param player: player num
        :param other_player: other player num
        :param depth: depth of recursion
        :param game: game simulator object
        :param col: given move column
        :return: the calculated score
        """
        row = game.get_free_row(col)

        game.make_move(col)

        sequences = game.created_sequences(row, col, player)
        local_score, seq_len = self.__best_sequence(sequences, game)

        # prevent irrelevant branching
        if seq_len < Game.SEQ_LENGTH:
            branch_score, _ = self.__best_score_move(other_player, depth - 1, game)
        else:
            branch_score = self.__GAME_OVER_FACTOR * (depth - 1)

        game.board[row][col] = 0

        return local_score, branch_score

    def __best_score_move(self, player, depth, game):
        """
        go over all possible moves for a current simulator status and return
        the one with the highest score.
        :param player: the player to calculate a move for
        :param depth: the number of moves to think ahead
        :param game: the game state
        :return: tuple of (best move score, move column number)
        """
        max_score = None
        best_move = 0

        if depth == 0:
            return 0, 0

        other_player = player % 2 + 1
        game.set_player(player)

        for col in range(Game.get_cols()):
            if game.get_player_at(0, col) is not None:
                continue

            local_score, branch_score = self.__get_location_value(
                player, other_player, depth, game, col)

            sum_score = local_score - branch_score

            if max_score is None or sum_score > max_score or (
                    sum_score == max_score and
                    abs(self.__mid - col) < abs(self.__mid - best_move)):
                max_score = sum_score
                best_move = col
            elif sum_score == max_score and \
                    abs(self.__mid - col) == abs(self.__mid - best_move):
                max_score, best_move = random.choice([(max_score, best_move),
                                                      (sum_score, col)])

        if max_score is None:
            max_score = 0

        game.set_player(other_player)
        return max_score, best_move

    def __best_move(self, player, depth, game):
        """
        the heart of the AI logic.
        this function will recursively dive calculating N (#depth) moves
        ahead - and try to maximise its own score, while minimizing the
        opponents score - by doing so it will try to keep the other player
        from winning, and try to win by itself.
        :param player:the player to calculate a move for
        :param depth: the number of moves to think ahead
        :param game: the game state
        :return: best move represented by column that is required to make the move
        """
        score, best_move = self.__best_score_move(player, depth, game)
        return best_move

    def __pre_run(self):
        """
        run some initial checks to make sure the ai should and can run
        :return:
        """
        if self.__game.get_current_player() != self.__player:
            raise ValueError("Wrong player.")

        free_cols = [col for col in range(Game.get_cols())
                     if self.__game.get_player_at(0, col) is None]

        if len(free_cols) == 0:
            raise ValueError("No possible AI moves.")

        return free_cols

    def find_legal_move(self, timeout=None):
        """
        this func will calculate several moves, that might be cut off by the
        timeout. calculates moves with rising complexity.
        :param timeout:
        :return:
        """
        free_cols = self.__pre_run()

        # idiot part:
        self.__last_found_move = 0
        self.__last_found_move = random.choice(free_cols)

        game_copy = GameSimulator(self.__game, player=self.__player)

        # kinda smart:
        self.__last_found_move = self.__best_move(self.__player, 1, game_copy)
        self.__last_found_move = self.__best_move(self.__player, 2, game_copy)

        # even smarter?
        self.__last_found_move = self.__best_move(self.__player, 5, game_copy)
        self.__last_found_move = self.__best_move(self.__player, 6, game_copy)

        return self.__last_found_move

    def get_last_found_move(self):
        """
        :return: last move calculated by find_legal_move
        """
        return self.__last_found_move

    def get_player(self):
        """
        return the ai's player number
        :return:
        """
        return self.__player
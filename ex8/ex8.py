X_CORD_START = 0
Y_CORD_START = -1
EMPTY = 0
FIRST_ROW = 0
RESET = 0
INC = 1
SQRT = 0.5
EMPTY_LIST = []
LENTGH_ONE = 1


def solve_sudoku(board):
    """
    this function will play the game sudoku for a given board
    :param board: board to play the game with - two dimensional array
    :return: true is solvable / false if unsolvable
    """
    unsolved_digits = {key: value for key, value in
                       enumerate(find_unsolved_digit(board))
                       if value < len(board)}
    # this is a dict to hold the digits that are not filled out completely
    # and how many remain to fill in the board.
    return recursive_placer(board, X_CORD_START, Y_CORD_START,
                            unsolved_digits)


def find_unsolved_digit(board):
    """
    this function will create a dict to tell how many digits are left to
    fill in a given board - to know how many have been filled out, and to
    not try to guess them in the backtracking.
    :param board: board to solve for
    :return: the dict num_occurrences that is created
    """
    num_occurrences = [EMPTY] * (len(board) + INC)
    for i in range(len(board)):
        for j in range(len(board[FIRST_ROW])):
            num_occurrences[board[i][j]] += INC
    return num_occurrences


def recursive_placer(board, i, j, unsolved_digits):
    """
    this function will actually place the "guesses" into the board.
    :param board:
    :param i:x position to guess for
    :param j:y position
    :param unsolved_digits:
    :return: tur if guess is valid, false if not valid
    """
    # for every digit in unsolved digits:

    # we want ro check a shura for the number we want to place
    # place it in an empty spot then place it there
    # check if it is valid
    # if valid, take one of the unsolved digits, and to the next shura
    # if invalid - next amuda
    # if invalid at all shurut - return false

    # this code will increases the coordinates to next position o the board
    if j < len(board) - INC:
        j += INC
    elif i < len(board[FIRST_ROW]) - INC:
        i += INC
        j = RESET
    else:
        return True  # board is done

    if board[i][j] != EMPTY:  # if there is some thing there
        return recursive_placer(board, i, j, unsolved_digits)

    # this will go though all the unsolved digits and try to place them
    for digit in unsolved_digits:
        if valid_placement(board, i, j, digit):
            board[i][j] = digit
            unsolved_digits[digit] -= INC
            if recursive_placer(board, i, j, unsolved_digits):
                return True  # works! next position
            else:  # if not valid return thr previous state and continue
                board[i][j] = EMPTY
                unsolved_digits[digit] += INC

    return False


def valid_placement(board, x, y, solution):
    """
    checks if the guess we placed is valid in the sodoku
    :param board:
    :param x: x position
    :param y: y position
    :param solution: our guess
    :return:
    """

    # rows/ columns check:
    SQRT_BOARD = int(len(board) ** SQRT)
    for i in range(len(board)):
        if board[i][y] == solution:
            return False

    for j in range(len(board[FIRST_ROW])):
        if board[x][j] == solution:
            return False

    # ss = shura of square = x//sqrtboard
    # sa = amuds of square = y//sqrtboard
    # shura within the square = x%sqrtboard
    # amuda within the sqire = y%sqrtboard

    # search in the square - (ss * sqrtboard)+1 < +4
    # search in the square - (sa * sqrtboard)+1 < +4

    # formula to check little square:
    square_x_position = int((x // SQRT_BOARD) * SQRT_BOARD)
    square_y_position = int((y // SQRT_BOARD) * SQRT_BOARD)

    for i in range(square_x_position, square_x_position + SQRT_BOARD):
        for j in range(square_y_position, square_y_position + SQRT_BOARD):
            if board[i][j] == solution:
                return False

    return True  # all checks went though


def print_k_subsets(n, k):
    """
    print all the subsets of 0- n-1 in k length
    :param n:
    :param k:
    :return:
    """
    for i in range(n):
        k_subset_helper([i], n, k)


def k_subset_helper(sub_sequences, n, k):
    """
    print all the subsets of 0- n-1 in k length
    :param sub_sequences:
    :param n:
    :param k:
    :return:
    """
    if len(sub_sequences) == k:  # if sub_sequences has gotten to the
        print(sub_sequences)  # printed, and then we are done here! return!
        return

    for i in range(max(sub_sequences) + INC, n):
        k_subset_helper(sub_sequences + [i], n, k)


def fill_k_subsets(n, k, lst):
    """
    calculates  all the subsets of 0- n-1 in k length
    :param n:
    :param k:
    :param lst:
    :return:
    """
    for i in range(n):
        fill_k_subsets_helper([i], n, k, lst)


def fill_k_subsets_helper(sub_sequences, n, k, lst):
    """
    calculates  all the subsets of 0- n-1 in k length
    :param sub_sequences:
    :param n:
    :param k:
    :param lst:
    :return:
    """
    if len(sub_sequences) == k:  # if sub_sequences has gotten to the size
        lst.append(sub_sequences)  # , and then we are done here!
        return

    for i in range(max(sub_sequences) + INC, n):
        fill_k_subsets_helper(sub_sequences + [i], n, k, lst)


def return_k_subsets(n, k):
    """
    calculates  all the subsets of 0- n-1 in k length
    :param n:
    :param k:
    :return:
    """
    lst = EMPTY_LIST[:]
    temp_lst = EMPTY_LIST[:]  # to avoid pointer problem later
    for i in range(n):
        temp_lst = return_k_subsets_helper([i], n, k)
        if k == LENTGH_ONE:  # different use
            lst.append(temp_lst)
        else:
            lst.extend(temp_lst)
    return lst  # return final product


def return_k_subsets_helper(sub_sequences, n, k):
    """
    calculates  all the subsets of 0- n-1 in k length
    :param sub_sequences:
    :param n:
    :param k:
    :return:
    """
    lst = EMPTY_LIST[:]
    if len(sub_sequences) == k:  # if sub_sequences has gotten to the size
        return sub_sequences  # , and then we are done here! return!

    for i in range(max(sub_sequences) + INC, n):
        lst.append(return_k_subsets_helper(sub_sequences + [i], n, k))

    return lst

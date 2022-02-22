################################################################
#                       Tester for ex8                         #
################################################################
# Move to the same folder with ex8 then run through the pytest #
# Nadav Har-Tuv                                                #
# nadav.har-tuv1@mail.huji.ac.il                               #
################################################################


import ex8
import io
import contextlib
import math


def matrix_transpose(original_mtr):
    """
    A function that transpose the matrix. replacing the rows and columns.
    :param original_mtr: list containing lists, the original matrix
    :return: list containing lists, the new matrix
    """
    new_mtr = []
    if len(original_mtr) > 0:
        for col in range(len(original_mtr[0])):
            list_to_add = []
            for row in range(len(original_mtr)):
                list_to_add.append(original_mtr[row][col])

            new_mtr.append(list_to_add)
    return new_mtr


def checking_full_sud(sud):
    for col in range(len(sud)):
        assert len(sud[col]) == len(set(sud[col]))
    sud = matrix_transpose(sud)

    for col in range(len(sud)):
        assert len(sud[col]) == len(set(sud[col]))

    big_squares = int(len(sud) ** 0.5)
    for big_col in range(big_squares):
        for big_row in range(big_squares):
            nums = set()
            for col in range(big_col * big_squares,
                             (big_col + 1) * big_squares):
                for row in range(big_row * big_squares,
                                 (big_row + 1) * big_squares):
                    assert sud[col][row] not in nums
                    nums.add(sud[col][row])


def not_changed_save_places(original, new):
    for col in range(len(new)):
        for row in range(len(new[0])):
            if original[col][row] != 0:
                assert original[col][row] == new[col][row]


def not_changed_at_all(original, new):
    for col in range(len(new)):
        for row in range(len(new[0])):
            assert original[col][row] == new[col][row]


def test_sudoku_of_empty_one():
    board = [[0]]
    assert ex8.solve_sudoku(board) is True
    assert board == [[1]]


def test_sudoku_of_fill_one():
    board = [[1]]
    assert ex8.solve_sudoku(board) is True
    assert board == [[1]]


def test_sudoku_of_empty_4():
    board = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    assert ex8.solve_sudoku(board) is True
    checking_full_sud(board)


def test_1_sudoku_of_4():
    board = [
        [1, 2, 3, 4],
        [3, 0, 0, 1],
        [4, 0, 0, 2],
        [2, 1, 4, 3]
    ]
    assert ex8.solve_sudoku(board) is True
    checking_full_sud(board)
    not_changed_save_places([
        [1, 2, 3, 4],
        [3, 0, 0, 1],
        [4, 0, 0, 2],
        [2, 1, 4, 3]
    ], board)


def test_2_sudoku_of_4():
    board = [
        [3, 0, 4, 0],
        [0, 1, 0, 3],
        [2, 3, 0, 0],
        [1, 0, 0, 2]
    ]

    assert ex8.solve_sudoku(board) is True
    checking_full_sud(board)
    not_changed_save_places([
        [3, 0, 4, 0],
        [0, 1, 0, 3],
        [2, 3, 0, 0],
        [1, 0, 0, 2]
    ], board)


def test_1_sudoku_of_bad_4():
    board = [
        [1, 2, 3, 0],
        [3, 0, 0, 4],
        [4, 0, 0, 2],
        [2, 1, 4, 3]
    ]
    assert ex8.solve_sudoku(board) is False
    not_changed_at_all([
        [1, 2, 3, 0],
        [3, 0, 0, 4],
        [4, 0, 0, 2],
        [2, 1, 4, 3]
    ], board)


def test_2_sudoku_of_bad_4():
    board = [
        [1, 2, 3, 0],
        [0, 0, 0, 4],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    assert ex8.solve_sudoku(board) is False
    not_changed_at_all([
        [1, 2, 3, 0],
        [0, 0, 0, 4],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ], board)


def test_sudoku_of_empty_9():
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]

    ]
    assert ex8.solve_sudoku(board) is True
    checking_full_sud(board)


def test_1_sudoku_of_9():
    board = [
        [0, 5, 2, 9, 0, 1, 3, 6, 0],
        [0, 8, 0, 0, 7, 0, 0, 0, 2],
        [0, 0, 4, 0, 0, 0, 0, 7, 1],
        [4, 1, 0, 0, 5, 9, 0, 0, 0],
        [0, 2, 0, 0, 6, 0, 0, 5, 0],
        [0, 0, 0, 2, 3, 0, 0, 8, 4],
        [5, 7, 0, 0, 0, 0, 6, 0, 0],
        [2, 0, 0, 0, 9, 0, 0, 1, 0],
        [0, 6, 9, 7, 0, 2, 8, 4, 0]
    ]
    assert ex8.solve_sudoku(board) is True
    checking_full_sud(board)
    not_changed_save_places([
        [0, 5, 2, 9, 0, 1, 3, 6, 0],
        [0, 8, 0, 0, 7, 0, 0, 0, 2],
        [0, 0, 4, 0, 0, 0, 0, 7, 1],
        [4, 1, 0, 0, 5, 9, 0, 0, 0],
        [0, 2, 0, 0, 6, 0, 0, 5, 0],
        [0, 0, 0, 2, 3, 0, 0, 8, 4],
        [5, 7, 0, 0, 0, 0, 6, 0, 0],
        [2, 0, 0, 0, 9, 0, 0, 1, 0],
        [0, 6, 9, 7, 0, 2, 8, 4, 0]
    ], board)


def test_2_sudoku_of_9():
    board = [
        [0, 0, 9, 0, 2, 0, 0, 3, 6],
        [0, 8, 5, 0, 0, 0, 0, 1, 7],
        [0, 0, 0, 0, 5, 7, 2, 0, 4],
        [5, 0, 0, 0, 0, 2, 0, 6, 0],
        [0, 6, 4, 3, 0, 8, 1, 2, 0],
        [0, 7, 0, 1, 0, 0, 0, 0, 9],
        [3, 0, 1, 7, 8, 0, 0, 0, 0],
        [4, 9, 0, 0, 0, 0, 8, 5, 0],
        [6, 2, 0, 0, 3, 0, 4, 0, 0]
    ]
    assert ex8.solve_sudoku(board) is True
    checking_full_sud(board)
    not_changed_save_places([
        [0, 0, 9, 0, 2, 0, 0, 3, 6],
        [0, 8, 5, 0, 0, 0, 0, 1, 7],
        [0, 0, 0, 0, 5, 7, 2, 0, 4],
        [5, 0, 0, 0, 0, 2, 0, 6, 0],
        [0, 6, 4, 3, 0, 8, 1, 2, 0],
        [0, 7, 0, 1, 0, 0, 0, 0, 9],
        [3, 0, 1, 7, 8, 0, 0, 0, 0],
        [4, 9, 0, 0, 0, 0, 8, 5, 0],
        [6, 2, 0, 0, 3, 0, 4, 0, 0]
    ], board)


def test_3_sudoku_of_9():
    board = [
        [9, 0, 5, 0, 0, 0, 0, 0, 8],
        [4, 0, 0, 5, 7, 0, 1, 0, 6],
        [0, 2, 7, 6, 0, 0, 0, 4, 0],
        [0, 9, 6, 0, 0, 3, 5, 1, 2],
        [7, 0, 4, 0, 1, 0, 3, 0, 0],
        [2, 1, 0, 9, 8, 0, 0, 0, 4],
        [0, 8, 1, 0, 0, 4, 0, 9, 0],
        [3, 0, 0, 8, 0, 0, 0, 5, 1],
        [0, 0, 2, 0, 0, 7, 0, 6, 0]
    ]
    assert ex8.solve_sudoku(board) is True
    checking_full_sud(board)
    not_changed_save_places([
        [9, 0, 5, 0, 0, 0, 0, 0, 8],
        [4, 0, 0, 5, 7, 0, 1, 0, 6],
        [0, 2, 7, 6, 0, 0, 0, 4, 0],
        [0, 9, 6, 0, 0, 3, 5, 1, 2],
        [7, 0, 4, 0, 1, 0, 3, 0, 0],
        [2, 1, 0, 9, 8, 0, 0, 0, 4],
        [0, 8, 1, 0, 0, 4, 0, 9, 0],
        [3, 0, 0, 8, 0, 0, 0, 5, 1],
        [0, 0, 2, 0, 0, 7, 0, 6, 0]
    ], board)


def test_1_sudoku_of_bad_9():
    board = [
        [6, 5, 2, 9, 0, 1, 3, 0, 0],
        [0, 8, 0, 6, 7, 0, 0, 0, 2],
        [0, 0, 4, 0, 0, 6, 0, 7, 1],
        [4, 1, 0, 0, 5, 9, 0, 6, 0],
        [0, 2, 0, 0, 6, 0, 0, 5, 0],
        [0, 0, 6, 2, 3, 0, 0, 8, 4],
        [5, 7, 0, 0, 0, 0, 6, 0, 0],
        [2, 0, 0, 0, 9, 0, 0, 1, 0],
        [0, 6, 9, 7, 0, 2, 8, 4, 0]
    ]
    assert ex8.solve_sudoku(board) is False
    not_changed_at_all([
        [6, 5, 2, 9, 0, 1, 3, 0, 0],
        [0, 8, 0, 6, 7, 0, 0, 0, 2],
        [0, 0, 4, 0, 0, 6, 0, 7, 1],
        [4, 1, 0, 0, 5, 9, 0, 6, 0],
        [0, 2, 0, 0, 6, 0, 0, 5, 0],
        [0, 0, 6, 2, 3, 0, 0, 8, 4],
        [5, 7, 0, 0, 0, 0, 6, 0, 0],
        [2, 0, 0, 0, 9, 0, 0, 1, 0],
        [0, 6, 9, 7, 0, 2, 8, 4, 0]
    ], board)


def test_2_sudoku_of_bad_9():
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 2, 3, 4, 0, 6, 7, 8, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 0, 0, 0, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    assert ex8.solve_sudoku(board) is False
    not_changed_at_all([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 2, 3, 4, 0, 6, 7, 8, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 0, 0, 0, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ], board)


def test_sudoku_of_empty_16():
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    assert ex8.solve_sudoku(board) is True
    checking_full_sud(board)


###########################################################################


def nCr(n, r):
    f = math.factorial
    return f(n) // (f(r) * f(n - r))


def capture_print(fun):
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        fun()
    retval = f.getvalue().strip().split("\n")
    if retval == [""]:
        return []
    return retval


def test_empty_print_k_subsets():
    assert capture_print(lambda: ex8.print_k_subsets(0, 0)) == []
    assert capture_print(lambda: ex8.print_k_subsets(0, 5)) == []


def test_1_print_k_subsets():
    assert sorted(capture_print(lambda: ex8.print_k_subsets(3, 1))) == ["[0]", "[1]",
                                                                "[2]"]
    assert sorted(capture_print(lambda: ex8.print_k_subsets(5, 1))) == [
        "[0]",
        "[1]",
        "[2]",
        "[3]",
        "[4]"]


def test_2_print_k_subsets():
    assert sorted(capture_print(lambda: ex8.print_k_subsets(3, 2))) == [
        "[0, 1]",
        "[0, 2]",
        "[1, 2]"]
    assert sorted(capture_print(lambda: ex8.print_k_subsets(5, 2))) == [
        "[0, 1]",
        "[0, 2]",
        "[0, 3]",
        "[0, 4]",
        "[1, 2]",
        "[1, 3]",
        "[1, 4]",
        "[2, 3]",
        "[2, 4]",
        "[3, 4]"]


def test_3_print_k_subsets():
    assert capture_print(lambda: ex8.print_k_subsets(3, 3)) == ["[0, 1, 2]"]
    result = capture_print(lambda: ex8.print_k_subsets(5, 3))
    assert len(result) == nCr(5, 3)
    assert len(result) == len(set(result))


def test_4_print_k_subsets():
    result = capture_print(lambda: ex8.print_k_subsets(10, 4))
    assert len(result) == nCr(10, 4)
    assert len(result) == len(set(result))


def test_1_return_k_subsets():
    assert sorted(ex8.return_k_subsets(3, 1)) == [[0], [1], [2]]
    assert sorted(ex8.return_k_subsets(5, 1)) == [
        [0],
        [1],
        [2],
        [3],
        [4]]


def test_2_return_k_subsets():
    assert sorted(ex8.return_k_subsets(3, 2)) == [[0, 1], [0, 2], [1, 2]]
    assert sorted(ex8.return_k_subsets(5, 2)) == [
        [0, 1],
        [0, 2],
        [0, 3],
        [0, 4],
        [1, 2],
        [1, 3],
        [1, 4],
        [2, 3],
        [2, 4],
        [3, 4]]


def test_3_return_k_subsets():
    assert ex8.return_k_subsets(3, 3) == [[0, 1, 2]]
    result = ex8.return_k_subsets(5, 3)
    assert len(result) == nCr(5, 3)
    result = [str(i) for i in result]
    assert len(result) == len(set(result))

#
# def test_4_return_k_subsets():
#     result = ex8.return_k_subsets(10, 4)
#     assert len(result) == nCr(10, 4)
#     result = [str(i) for i in result]
#     assert len(result) == len(set(result))


def test_1_fill_k_subsets():
    tot_list = []
    assert ex8.fill_k_subsets(3, 1, tot_list) is None
    assert sorted(tot_list) == [[0], [1], [2]]

    tot_list = []
    assert ex8.fill_k_subsets(5, 1, tot_list) is None
    assert sorted(tot_list) == [
        [0],
        [1],
        [2],
        [3],
        [4]]


def test_2_fill_k_subsets():
    tot_list = []
    assert ex8.fill_k_subsets(3, 2, tot_list) is None
    assert sorted(tot_list) == [[0, 1], [0, 2], [1, 2]]

    tot_list = []
    assert ex8.fill_k_subsets(5, 2, tot_list) is None
    assert sorted(tot_list) == [
        [0, 1],
        [0, 2],
        [0, 3],
        [0, 4],
        [1, 2],
        [1, 3],
        [1, 4],
        [2, 3],
        [2, 4],
        [3, 4]]


def test_3_fill_k_subsets():
    tot_list = []
    assert ex8.fill_k_subsets(3, 3, tot_list) is None
    assert tot_list == [[0, 1, 2]]

    tot_list = []
    ex8.fill_k_subsets(5, 3, tot_list) is None
    assert len(tot_list) == nCr(5, 3)
    result = [str(i) for i in tot_list]
    assert len(result) == len(set(result))


def test_4_fill_k_subsets():
    tot_list = []
    assert ex8.fill_k_subsets(10, 4, tot_list) is None
    assert len(tot_list) == nCr(10, 4)
    result = [str(i) for i in tot_list]
    assert len(result) == len(set(result))


def test_sudoku_of_16():
    board = [
        [0, 15, 0, 1, 0, 2, 10, 14, 12, 0, 0, 0, 0, 0, 0, 0],
        [0, 6, 3, 16, 12, 0, 8, 4, 14, 15, 1, 0, 2, 0, 0, 0],
        [14, 0, 9, 7, 11, 3, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 13, 2, 12, 0, 0, 0, 0, 6, 0, 0, 0, 0, 15, 0, 0],
        [0, 0, 0, 0, 14, 1, 11, 7, 3, 5, 10, 0, 0, 8, 0, 12],
        [3, 16, 0, 0, 2, 4, 0, 0, 0, 14, 7, 13, 0, 0, 5, 15],
        [11, 0, 5, 0, 0, 0, 0, 0, 0, 9, 4, 0, 0, 6, 0, 0],
        [0, 0, 0, 0, 13, 0, 16, 5, 15, 0, 0, 12, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 1, 12, 0, 8, 3, 10, 11, 0, 15, 0],
        [2, 12, 0, 11, 0, 0, 14, 3, 5, 4, 0, 0, 0, 0, 9, 0],
        [6, 3, 0, 4, 0, 0, 13, 0, 0, 11, 9, 1, 0, 12, 16, 2],
        [0, 0, 10, 9, 0, 0, 0, 0, 0, 0, 12, 0, 8, 0, 6, 7],
        [12, 8, 0, 0, 16, 0, 0, 10, 0, 13, 0, 0, 0, 5, 0, 0],
        [5, 0, 0, 0, 3, 0, 4, 6, 0, 1, 15, 0, 0, 0, 0, 0],
        [0, 9, 1, 6, 0, 14, 0, 11, 0, 0, 2, 0, 0, 0, 10, 8],
        [0, 14, 0, 0, 0, 13, 9, 0, 4, 12, 11, 8, 0, 0, 2, 0]
    ]

    assert ex8.solve_sudoku(board) is True
    assert board == [
        [8, 15, 11, 1, 6, 2, 10, 14, 12, 7, 13, 3, 16, 9, 4, 5],
        [10, 6, 3, 16, 12, 5, 8, 4, 14, 15, 1, 9, 2, 11, 7, 13],
        [14, 5, 9, 7, 11, 3, 15, 13, 8, 2, 16, 4, 12, 10, 1, 6],
        [4, 13, 2, 12, 1, 9, 7, 16, 6, 10, 5, 11, 3, 15, 8, 14],
        [9, 2, 6, 15, 14, 1, 11, 7, 3, 5, 10, 16, 4, 8, 13, 12],
        [3, 16, 12, 8, 2, 4, 6, 9, 11, 14, 7, 13, 10, 1, 5, 15],
        [11, 10, 5, 13, 8, 12, 3, 15, 1, 9, 4, 2, 7, 6, 14, 16],
        [1, 4, 7, 14, 13, 10, 16, 5, 15, 6, 8, 12, 9, 2, 3, 11],
        [13, 7, 16, 5, 9, 6, 1, 12, 2, 8, 3, 10, 11, 14, 15, 4],
        [2, 12, 8, 11, 7, 16, 14, 3, 5, 4, 6, 15, 1, 13, 9, 10],
        [6, 3, 14, 4, 10, 15, 13, 8, 7, 11, 9, 1, 5, 12, 16, 2],
        [15, 1, 10, 9, 4, 11, 5, 2, 13, 16, 12, 14, 8, 3, 6, 7],
        [12, 8, 4, 3, 16, 7, 2, 10, 9, 13, 14, 6, 15, 5, 11, 1],
        [5, 11, 13, 2, 3, 8, 4, 6, 10, 1, 15, 7, 14, 16, 12, 9],
        [7, 9, 1, 6, 15, 14, 12, 11, 16, 3, 2, 5, 13, 4, 10, 8],
        [16, 14, 15, 10, 5, 13, 9, 1, 4, 12, 11, 8, 6, 7, 2, 3]
    ]


from wordsearch import lines_checker, read_matrix_file


def lines_checker_checker():
    matrix = read_matrix_file("mat.txt")
    tests = [None] * 10
    tests[0] = lines_checker("aaa", matrix, "u") == 0

    matrix = read_matrix_file("mat2.txt")
    tests[1] = lines_checker("bob", matrix, "u") == \
               lines_checker("bob", matrix, "d") == 4
    tests[2] = lines_checker("bob", matrix, "l") == \
               lines_checker("bob", matrix, "r") == 2
    tests[3] = lines_checker("bob", matrix, "z") == \
               lines_checker("bob", matrix, "w") == 2
    tests[4] = lines_checker("bob", matrix, "x") == \
               lines_checker("bob", matrix, "y") == 1

    matrix = read_matrix_file("mat3.txt")
    tests[5] = lines_checker("aaa", matrix, "r") == \
               lines_checker("aaa", matrix, "l") == 18
    tests[6] = lines_checker("aaa", matrix, "u") == \
               lines_checker("aaa", matrix, "d") == 20
    tests[7] = lines_checker("aaa", matrix, "x") == \
               lines_checker("aaa", matrix, "y") == \
               lines_checker("aaa", matrix, "z") == \
               lines_checker("aaa", matrix, "w") == 12

    matrix = read_matrix_file("mat4.txt")
    tests[8] = lines_checker("bobcat", matrix, "l") == \
               lines_checker("cat", matrix, "l") == 1 and \
               lines_checker("bob", matrix, "l") == \
               lines_checker("bob", matrix, "r") == 4
    tests[9] = lines_checker("atacbobobobob"[::-1], matrix, "l") == \
               lines_checker("atacbobobobob", matrix, "r") == 1

    for test in tests:
        if not test:
            return False
    return True


if __name__ == "__main__":
    if lines_checker_checker():
        print("all good with code!!!")
    else:
        print("oh no...")

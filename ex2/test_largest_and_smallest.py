from largest_and_smallest import largest_and_smallest

TEST_MSG = "Function 'largest and smallest' has succeeded in "

def definitely_not_foo():
    """
    this func tests the previous program "largest_and_smallest" to see if
    it can handle all sort of different inputs, and still return the right
    answer.
    :return: returns the number of tests the programs succeeded in
    """
    test1 = (largest_and_smallest(0, 10, 3) == (10, 0))  # how to handle 0
    test2 = (largest_and_smallest(1, -1, 3) == (3, -1))  # how to handle
    # negative
    test3 = (largest_and_smallest(0.1, 10, 99.1) == (99.1, 0.1))  # floats
    test4 = (largest_and_smallest(0.00000000009, 2, 9999999999) == (
        9999999999, 0.00000000009))
    # very large number, snd very small number

    return int(test1) + int(test2) + int(test3) + int(test4)

if __name__ == "__main__":
    print(TEST_MSG, definitely_not_foo(), " out of 4 tests")
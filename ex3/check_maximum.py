from ex3 import maximum

NUMBER_OF_TESTS = 6

def test():
    """
    func to test the func maximum - it gives it values, and checks whether
    the function behaves correctly.
    :return: if all the tests went correctly - true/ false.
    """
    tests = [None] * NUMBER_OF_TESTS  # creates a list with length 6
    tests[0] = maximum([1, 2, 3]) == 3  # test a normal input
    tests[1] = maximum([-4, 2, 3]) == 3  # test with a negative number
    tests[2] = maximum([]) == None # tests an empty list
    tests[3] = maximum([4.5, 2, 3]) == 4.5 # test with a float
    tests[4] = maximum([3, 3, 3]) == 3  # test when all number in list are
    # the same
    tests[5] = maximum([0, 3, 4]) == 4  # test with a zero in the list

    all_successful = True  # parameter to see if all the tests went correctly

    for index in range(len(tests)):
        print("test number: "+str(index)+" was successful: " + str(tests[
                                                                    index]))
        all_successful = ((all_successful and tests[index]) == True)
        #  if even one test returned false, then the var will be false.
        # will be true only if ALL the tests went correctly.

    return all_successful

############MAIN##################

if __name__ == '__main__':
    test()

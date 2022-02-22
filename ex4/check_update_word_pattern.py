from hangman import update_word_pattern
NUMBER_TESTS = 6

def so_called_foo():
    """
    function to test the function update_word_pattern
    :return: if passed all test.
    """
    tests = [None] * NUMBER_TESTS
    tests[0] = update_word_pattern("aaaaaaa", "_______", "a") == "aaaaaaa"
    tests[1] = update_word_pattern("", "", "") == ""
    tests[2] = update_word_pattern("___", "___", "_") == "___"
    tests[3] = update_word_pattern("123", "_2_", "1") == "12_"
    tests[4] = update_word_pattern("abcabcabc", "_________", "a") == \
                                   "a__a__a__"
    tests[5] = update_word_pattern("a", "_", "a") == "a"
    return not False in tests  # if even one false - return false.


if __name__ == "__main__":
    if so_called_foo:
        print("All successful !!")
    else:
        print("Something failed :(")
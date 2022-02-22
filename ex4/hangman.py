import PIL as pil
import hangman_helper

CHAR_A = 97  # ASCII value of the letter a
ALPHABET = 26  # number of letters in the english alphabet


def update_word_pattern(word, pattern, letter):
    """
    this func takes a pattern of the game hangman and updates it according
    to the given "new letter". if the letter appears, it adds it to the
    pattern and returns it, if not, it just returns the previous pattern.
    :param word: the random word for thee game hangman
    :param pattern: the current state of the user -  a pattern of the
    guessed letters in the word.
    :param letter: the guessed "new letter" to check if in the word.
    :return:a new pattern to the user.
    """
    new_pattern = ""  # new pattern to be returned.
    for index in range(len(word)):  # loop the letters of the word
        if word[index] == letter:
            new_pattern += letter  # if found guessed letter in the word,
            # them update the pattern accordingly.
            continue  # next letter to check!
        new_pattern += pattern[index]  # if got here then we didn't find a
        # letter, so just add whatever was already guessed\not guessed in
        #  the given pattern
    return new_pattern


def nice_input(tested_input):
    """
    check whether the input is valid(a nice input :) )
    input should be a single character - no numbers, no words, just 1 char.
    :param tested_input: the input the user put in the input box
    :return:whether the input is valid - true\ false
    """
    letters_in_alpha_bet = [None] * ALPHABET  # all the letters of the
    # english alphabet!
    for letter in range(len(letters_in_alpha_bet)):
        letters_in_alpha_bet[letter] = index_to_letter(letter)  # add all
        # the letters of the english alphabet into the list

    if tested_input not in letters_in_alpha_bet:
        return False  # if the input is not a single letter from the
        # alphabet - its not valid
    return True  # all good!


def run_single_game(word_list):
    """
    runs a single instance of the game hangman
    :param word_list: list of words to use in the game
    :return: nothing
    """
    rand_word = hangman_helper.get_random_word(word_list)  # random word
    # list generated
    wrong_guessing_list = []  # all the wrong guesses the user inputted
    error_count = 0  # error counter
    msg_to_user = hangman_helper.DEFAULT_MSG
    pattern = "_" * len(rand_word)  # pattern the user is shown

    while error_count < hangman_helper.MAX_ERRORS:  # while the user still
        # has guesses
        hangman_helper.display_state(pattern, error_count,
                                     wrong_guessing_list,
                                     msg_to_user)
        # function to display the state of the game
        kind_of_input, detail_input = hangman_helper.get_input()
        # input from the user, in the format - witch king of input(letter,
        # hint, finish game) , witch letter\ true\ false...
        if kind_of_input == hangman_helper.HINT:  # if the user asks for a
            # hint
            hangman_helper.NO_HINTS_MSG = choose_letter(filter_words_list(
                word_list, pattern, wrong_guessing_list), pattern)
            # get the hint with filtering all the possible words first
            # (filter_words_list), and passing that list into choose letter
            # function, witch decides on the "best" letter to choose.
            msg_to_user = hangman_helper.NO_HINTS_MSG
            continue  # next turn
        # other kind input checks.
        if kind_of_input == hangman_helper.LETTER and (not nice_input(
                detail_input)):  # if the kind of input is a letter,
            # and the input is valid(nice_input checks it and returns true\
            #  false)
            continue  # bad input! not nice:( next turn!

        # if we got here: letter input correct
        if detail_input in pattern or detail_input in wrong_guessing_list:
            # if letter already in pattern or in wrong_guessing_list,
            # then you already picked that letter - choose again!
            msg_to_user = hangman_helper.ALREADY_CHOSEN_MSG \
                                         + detail_input
            continue  # next turn!
        if detail_input in rand_word:  # if the chosen letter is in
            # rand_word then we should handle the update
            pattern = update_word_pattern(rand_word, pattern, detail_input)
            if pattern == rand_word:  # win case?
                msg_to_user = hangman_helper.WIN_MSG  # win
                # case!
                break  # get out of loop
            continue  # not win :(  next turn!

        # if we got here that means we guessed a wrong letter :(
        wrong_guessing_list.append(detail_input)  # add the wrong letter to
        #  the wrong_guessing_list
        error_count += 1  # and add to error count
        # hangman_helper.DEFAULT_MSG = rand_word ##################
    else:  # didn't win
        # if we got here then we ended the while loop above, that means we
        # lost, because we hit the max error amount :(
        msg_to_user = hangman_helper.LOSS_MSG + rand_word
    # in this place the output message of winning\ loosing is correct
    hangman_helper.display_state(pattern, error_count, wrong_guessing_list,
                                 msg_to_user, True)


def pattern_match(word, pattern):
    """
    checks wheter the pattern mathes a givven word - the chars that are
    not "_", are the same chars in the word(same index)
    :param word: random word to check againts
    :param pattern: the given pattern from the game( shown to the user)
    :return: true\ false, regarding them being matched.
    """
    for index in range(len(word)):
        if pattern[index] != "_" and pattern[index] != word[index]:
            return False  # found different char in same index.
    return True  # went though all and didn't find any differences.


def has_wrong_letter(word, wrong_guess_lst):
    """
    checks if a word contains a letter from the wrong guesses list
    :param word: word to check
    :param wrong_guess_lst: list of wrong guesses
    :return: true\ false - regarding having a wrong letter in the word
    """
    for wrong_char in wrong_guess_lst:
        if wrong_char in word:
            return True  # found wrong letter
    return False  # didn't find


def filter_words_list(words, pattern, wrong_guess_lst):
    """
    filters a given word list to have only words that match the pattern,
    and don't have any of the letters in the wrong guesses list
    :param words: list of words
    :param pattern: pattern to check matching with
    :param wrong_guess_lst: list of wrong guessed letters to filter out
    :return: new FILTERED list of words that match the pattern,
    and don't have any of the letters in the wrong guesses list
    """
    new_words = []  # filtered word list
    for word in words:
        if (len(word) == len(pattern) and pattern_match(word, pattern)
                and not has_wrong_letter(word, wrong_guess_lst)):  #
            # according to the filtering condition in the doc string.
            new_words.append(word)  # add the filtered word
    return new_words


def letter_to_index(letter):
    """
    Return the index of the given letter in an alphabet list.
    """
    return ord(letter.lower()) - CHAR_A


def index_to_letter(index):
    """
    Return the letter corresponding to the given index.
    """
    return chr(index + CHAR_A)


def choose_letter(words, pattern):
    """
    given a list of words, and a pattern, the function will return the
    letter that has the most instances in the list.
    :param words: list of words
    :param pattern: pattern from game
    :return:letter that has the most instances in the list.
    """
    letter_index = [0] * ALPHABET  # list that will contain instances of
    # each letter in the english alphabet
    for word in words:
        if len(word) == len(pattern):  # if the word length is matched
            for letter in word:
                if (letter not in pattern):  # the chosen letter should not
                    #  appear already in the given pattern
                    letter_index[letter_to_index(letter)] += 1
                    # add an instance
    # we should now return the letter with the max instances.
    # so we get the index with the max value - and convert it back to a
    # letter with index_to_letter. - return that letter.
    return index_to_letter(letter_index.index(max(letter_index)))


########################################################################
def main():
    """
    func to run the entire game.
    """
    word_for_game = hangman_helper.load_words()
    run_single_game(word_for_game)
    kind_of_input, detail_input = hangman_helper.get_input()
    while kind_of_input == hangman_helper.PLAY_AGAIN and detail_input == True:
        # while the input is to play again - run the game, and then ask again.
        run_single_game(word_for_game)
        kind_of_input, detail_input = hangman_helper.get_input()

if __name__ == "__main__":
    # print(filter_words_list(hangman_helper.load_words(), "_l_", []))
    # print(letter_to_index("a"))
    # print(choose_letter(hangman_helper.load_words(), "_________"))
    # print(choose_letter(["grape", "graee", "aaaaa"], "_____"))
    # print(has_letter(["apple"], "___a_"))
    hangman_helper.start_gui_and_call_main(main)  # run the entire game!!!
    hangman_helper.close_gui()  # close the game :(

import sys
import os

INVALID_NUM_OF_ARGS = "Error! User didn't input the correct amount of " \
                      "arguments into program! Must input 4 arguments!"
INVALID_PATH_CHOSEN_WORDS = "Error! Words file path is invalid"
INVALID_PATH_CHOSEN_MAT = "Error! Matrix file path is invalid"
INVALID_SEARCH_DIRECTIONS = "Error! Invalid search directions! Only allowed" \
                            "to use u d r l w x y z"
UP = "u"
DOWN = "d"
LEFT = "l"
RIGHT = "r"
DIAGNOL = "y"
REV_DIAGNOL = "x"
DOWN_TO_UP_RIGHT = "w"
UP_TO_DOWN_LEFT = "z"

REGULAR_STEP_DIRECTION = 1
COMMA = ","
NEW_LINE = "\n"

FIRST_PAIR = 0
SECOND_PAIR = 1

VALUE_SIDE_TO_SIDE = 0
VALUE_UP_AND_DOWN = 1
VALUE_DIAGONAL = 2
REV_VALUE_DIAGONAL = 3
STRT_LN = 0
END_LN = 1
STRT_CLM = 2
END_CLM = 3


def check_input_args(args1, args2, args3, args4):
    """
    checks for valid input:
    :param args: list of strings with the following requirments:
    [0] = words_path = path of the words file(has to exist already)
    [1] = mat_path = path of the matrix of words file(has to exist)
    [2] = output_path = path of the output of the program
    [3] = search_dirs = strinf of letters, that indicate the search
    directions of the words in the matrix.
    :return: Error message, or None in case of valid input.
    """
    valid_dirs = [UP, DOWN, "r", LEFT, DOWN_TO_UP_RIGHT, DIAGNOL, REV_DIAGNOL,
                  UP_TO_DOWN_LEFT]  # the valid
    # directions
    if not (args1 and args2 and args3 and args4):  # should be exactly 4
        # arguments
        # $$$$$$$$$$$$$$$$4$$$$$
        return INVALID_NUM_OF_ARGS

    if not os.path.exists(args1):
        return INVALID_PATH_CHOSEN_WORDS
    if not os.path.exists(args2):
        return INVALID_PATH_CHOSEN_MAT

    search_dir = args4

    for letter in search_dir:
        if letter not in valid_dirs:  # in case even one is invalid dir
            return INVALID_SEARCH_DIRECTIONS


def read_wordlist_file(filename):
    """
    converts a text file into a list
    :param filename: path of txt file
    :return: a list of every line in the file
    """
    wordlist = []
    with open(filename, "r") as file_wordlist:
        for line in file_wordlist:
            wordlist.append(
                line[:len(line) - 1])  # adds the word to the list,
            # and gets rid of the \n character.
    return wordlist


def read_matrix_file(filename):
    """
    converts a file into a matrix list
    :param filename: path of file to convert
    :return: matrix of every line split into a matrix
    """
    matrix = []
    with open(filename, "r") as file_mat:
        for line in file_mat:
            matrix.append(line[:len(line) - 1].split(","))  # adds the line
            # to  the list(splitted by ","),and gets rid of the \n character.
    return matrix


def match(word, matrix, row_index, column_index, direction):
    """
    a function that, given a matrix and a location in it(i,j coordinates),
    and a direction, searches for the given direction for the word.

    this function can "look" in all directions - it dynamically handles
    all directions. therefore there are  some things to understand,
    my function can only search for words in half of the
    directions, for the other complimenting half, it uses the reverse of
    the word to look - and so it can search through all the options.
    :param word: word to find in matrix
    :param matrix: matrix to find word in
    :param row_index: "x coordinate" in matrix
    :param column_index: "y coordinate" in matrix
    :param direction: the "direction" to loop for
    :return: how many words found in given direction
    """

    # complimenting direction witch will look for by flipping the word
    if direction == LEFT or direction == UP or direction == DIAGNOL \
            or direction == UP_TO_DOWN_LEFT:
        word = word[::-1]  # creating the flipped word

    return_value = 0  # how many we found
    offset_one = 0  # var to offset the checking of the matrix for the word
    for offset_two in range(len(word)):  # loop in the words length-to
        # compare & find it
        if direction == DOWN or direction == UP:
            offset_one = offset_two  # in these directions we need to increase
            offset_two = 0  # columns, not the rows. - rows stay the same.
        elif direction == DIAGNOL or direction == REV_DIAGNOL:
            # in these directions we need to go diagonally - increase rows
            # and columns
            offset_one = offset_two
        elif direction == UP_TO_DOWN_LEFT or direction == DOWN_TO_UP_RIGHT:
            offset_one = -offset_two
            # in these directions we
            # need to go in the "flipped" diagonal -
            # "backwards" and increase offset_one, while decreasing
            # offset_two the same amount.
        if word[max(offset_one, offset_two)] != \
                matrix[row_index + offset_one][column_index + offset_two]:
            break
        # here we check if we found even a single character out of order -
        # break. if ALL the loop tests went though - the word has been found!
        # * the max(offset_one, offset_two) is to keep the var coordinate
        # at the right index, so it wont be 0, while other tests are running.
    else:
        #  if we got here that means all the test went though and that
        # means we found a the word! can add 1 to the return_value
        return_value += 1
    return return_value


def vals_for_loop(word_len, matrix_getlengh0, matrix_getlengh1, direction):
    """
    this function will determine what the values the for loop for the
    checking mechanism will be. because my code is designed in a way that a
    single function will handle all direction of search, i have to maintain at
    witch values the for loop will run - this function helps find those
    values and returns them
    :param word_len: len of the word to search
    :param matrix_getlengh0: length of the matrix in the x direction
    :param matrix_getlengh1: length of the matrix in the y direction
    :param direction: direction of search
    :return: values for the for loop in the next function.
    """
    #  this "kavua" is not set at the start of the program because,
    # is depends on the inputs:
    VALUES_FOR_LOOP = [
        [0, matrix_getlengh0, 0, matrix_getlengh1 - word_len + 1]
        , [0, matrix_getlengh0 - word_len + 1, 0, matrix_getlengh1],
        [0, matrix_getlengh0 - word_len + 1, 0,
         matrix_getlengh1 - word_len + 1],
        [matrix_getlengh0 - 1, word_len - 2, 0,
         matrix_getlengh1 - word_len + 1]]
    # those are different options for the for loop, by the different search
    # directions, by the order -
    # [start position #for1(lines in matrix), end position #for1,
    # start position #for2(columns in matrix), end position #for2]

    # the following variables are the setting of the checking system -
    # they are there to keep the index in range of the matrix and just
    # defaults, and can change according to the chosen direction.
    # the default dir is "r"\ "l"
    start_line = VALUES_FOR_LOOP[VALUE_SIDE_TO_SIDE][STRT_LN]
    # index row to start searching
    end_line = VALUES_FOR_LOOP[VALUE_SIDE_TO_SIDE][END_LN]
    # index row to end searching
    start_column = VALUES_FOR_LOOP[VALUE_SIDE_TO_SIDE][STRT_CLM]
    # index col to start searching
    end_column = VALUES_FOR_LOOP[VALUE_SIDE_TO_SIDE][END_CLM]
    # index col to stop searching
    step_line = REGULAR_STEP_DIRECTION  # step of the search
    step_column = REGULAR_STEP_DIRECTION  # always stays 1, but to keep
    # consistent.. in the right\ left direction columns have to carefully
    # handled as to not go out of bounds.

    if direction == UP or direction == DOWN:  # setting for UP\DOWN directions
        end_line = VALUES_FOR_LOOP[VALUE_UP_AND_DOWN][END_LN]
        end_column = VALUES_FOR_LOOP[VALUE_UP_AND_DOWN][END_CLM]
        # in the up\ down direction rows have to carefully handled as to
        # not go out of bounds.
    elif direction == DIAGNOL or direction == REV_DIAGNOL:
        end_line = VALUES_FOR_LOOP[VALUE_DIAGONAL][END_LN]
        end_column = VALUES_FOR_LOOP[VALUE_DIAGONAL][END_CLM]
        # in the diagonal directions rows AND columns have to carefully
        # handled as to not go out of bounds.
    elif direction == DOWN_TO_UP_RIGHT or direction == UP_TO_DOWN_LEFT:
        start_line = VALUES_FOR_LOOP[REV_VALUE_DIAGONAL][STRT_LN]
        end_line = VALUES_FOR_LOOP[REV_VALUE_DIAGONAL][END_LN]
        step_line = - REGULAR_STEP_DIRECTION
        # in the flipped diagonal directions rows AND columns have to
        # carefully handled as to not go out of bounds.
        # but also we need to flip one axis of checking - i chose to slip
        # the rows, but it doesnt matter since i mirror them latter.
    return (start_line, end_line, start_column, end_column, step_line,
            step_column)


def lines_checker(word, matrix, direction):
    """
    given a certain direction this function will look for the word in the
    matrix in all the possible "lines" of the matrix that satisfy the
    direction, and count the number of instances.
    note: this function just like match, will work dynamically to look in
    all directions and so it has dynamically chosen variables to account for
    all uses,
    :param word: word to look for
    :param matrix: matrix to search in
    :param direction: direction to look
    :return: num of instances the word has appeared in the given direction
    """

    finder_counter = 0  # number of instances the word has benn founds

    # the next piece of code, will run a dynamic for loop on the matrix to
    # find the word. in order to maintain the for loop so it wont go out
    # of bounds, we have to set the for parameters dynamically - this function
    #  will set the parameters according to the direction given
    start_line, end_line, start_column, end_column, step_line, step_column = \
        vals_for_loop(len(word), len(matrix), len(matrix[0]), direction)

    # simple nested loop to run the checking func to find the word in the
    # given direction - uses the match func to sum the number of times the
    # word has appeared.
    for row_index in range(start_line, end_line, step_line):
        for column_index in range(start_column, end_column, step_column):
            finder_counter += match(word, matrix, row_index, column_index,
                                    direction)
    # finder_counter returns the number of instances the word hs appeared in
    #  the matrix in the given direction
    return finder_counter


def find_words_in_matrix(word_list, matrix, directions):
    """
    this func will create a list of tuples, that record the number of
    times a words off a list has appeared in the matrix, in chosen
    directions - will record only word that appeared at least once.
    :param word_list: list of words to check appearance in matrix
    :param matrix: matrix to check against
    :param directions: directions to look in - can be several directions
    :return: list of tuples - a word that has been found, number of
    appearances
    """
    found = 0
    words_found_in_matrix = []  # list to contain the word that are found
    for word in word_list:  # all words
        for dir in directions:  # all direction given
            found += lines_checker(word, matrix, dir)
        if found:
            words_found_in_matrix.append((word, found))
        found = 0
        # tuple structure = (word, number of times in matrix in direction)
    return words_found_in_matrix


def write_output_file(results, output_filename):
    """
    this func will write an output file(for the results if the game) to a
    given path.
    :param results: the results of the game - found word, number of times.
    :param output_filename: the path to save the file at.
    """
    with open(output_filename,
              DOWN_TO_UP_RIGHT) as output_file:  # if exists - rewrite,
        # if not - make a new file in the path given to the function.
        for pair in results:
            output_file.write(pair[FIRST_PAIR] + COMMA +
                              str(pair[SECOND_PAIR]) + NEW_LINE)
            # result in every line.


def run_puzzle(args1, args2, args3, args4):
    """
    this function runs the entire game!
    """
    input_valid = check_input_args(args1, args2, args3, args4)
    if input_valid is not None:
        print(input_valid)
        return  # checks if the input is correct

    #  if input is correct - put the values into the variables
    wordlist = read_wordlist_file(args1)
    matrix = read_matrix_file(args2)
    output_path = args3
    directions = args4
    # running the search function
    pairs = find_words_in_matrix(wordlist, matrix, directions)
    # output to txt file.
    write_output_file(pairs, output_path)


################################MAIN########################################

if __name__ == "__main__":
    run_puzzle(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

import tempfile
import json
from subprocess import Popen, PIPE

# These don't test the 'game' class itself(as there isn't much to test),
# they test the entire game

PYTHON_PROC_ARGS = ["python", "../../game.py"]


def create_car_config(cars_dict):
    with tempfile.NamedTemporaryFile(delete=False) as file:
        file.write(bytes(json.dumps(cars_dict), 'UTF-8'))
        return file.name


def assert_finishes_with_moves(cfg_file, moves):
    """
    Ensures that the game finishes after consuming all given moves(no more and
     no less)

    :param cfg_file: Path to a car_config.json file
    :param moves: List of strings in the form "R,r"
    """
    proc_args = PYTHON_PROC_ARGS + [cfg_file]
    # hacky way of determining if the game terminates after exactly all moves
    # were given:

    # First, we expect an EOF error, as we haven't won yet and the game should
    #  ask for another step.
    failing_moves = "\n".join(moves[:-1])
    _out, err = Popen(proc_args, universal_newlines=True, stdin=PIPE,
                      stderr=PIPE, stdout=PIPE).communicate(failing_moves)
    assert "EOF" in err, "Game should've raised an EOF error as we've quit " \
                         "before providing all moves. got: " + err

    # Now, we expect no error(graceful termination of the game) after all valid
    #  moves have been given.
    success_moves = "\n".join(moves)
    _out, err = Popen(proc_args, universal_newlines=True, stdin=PIPE,
                      stderr=PIPE, stdout=PIPE).communicate(success_moves)
    assert len(
        err) == 0, "Game did not terminate successfully after giving all valid" \
                   " moves. got: " + err


def assert_fails_with_moves(cfg_file, moves):
    """
    Ensures that the game hasn't finished after these moves

    :param cfg_file: Path to a car_config.json file
    :param moves: List of strings in the form "R,r"
    """
    proc_args = PYTHON_PROC_ARGS + [cfg_file]
    moves_st = "\n".join(moves)
    _out, err = Popen(proc_args, universal_newlines=True, stdin=PIPE,
                      stderr=PIPE, stdout=PIPE).communicate(moves_st)
    assert "EOF" in err, f"Expected game to fail(EOF) when given moves " \
                         f"{moves}," f"but it terminated as if we've won."


def test_valid_simple():
    cars = {
        "R": [2, [3, 0], 1],
        "O": [3, [1, 4], 0]
    }

    cfg_file = create_car_config(cars)
    assert_finishes_with_moves(cfg_file, ["O,u"] + ["R,r"] * 6)
    assert_finishes_with_moves(cfg_file,
                               ["O,u"] + ["R,r"] * 5 + ["R,l", "R,r", "R,r"])
    assert_finishes_with_moves(cfg_file,
                               ["O,u"] + ["Invalid,Cowabunga"] * 20 + [
                                   "O,u"] * 1337 + ["R,r"] * 6)
    assert_fails_with_moves(cfg_file, ["O,u"] + ["R,r"] * 2)
    assert_fails_with_moves(cfg_file, ["O,u"] + ["R,r"] * 1)

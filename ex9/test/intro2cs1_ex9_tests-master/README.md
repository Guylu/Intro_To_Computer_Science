# Tests for exercise 9 - Rush Hour

## Description

These are tests for the rush hour game.

Note that these tests aren't guaranteed to be correct, it's very likely that I've
made mistakes, misunderstood some parts of the exercise or added unnecessary
constraints. If so, please 
[open up an issue](https://github.cs.huji.ac.il/danielkerbel/intro2cs1_ex9_tests/issues)
or correct them and make a pull request.

If you don't understand why a test failed, open up the test file and see what's
going on. I've tried to keep the tests somewhat simple and descriptive.

## Contributing
If you found a mistake or want to add your own tests, feel free to do so (via basic git usage
and a pull request, see tutorials on the web)


## What is/isn't covered
Covered:
* API of Car
* API of Board
* A pretty simple test of one valid playthrough of the game

Not covered:
* More interesting playthroughs or edge-cases
* Doesn't enforce correct usage of the API - e.g by replacing your own class
  implementations with alternative ones.
  
## Usage

Requires 'pytest' to be available in your environment. Can be installed via `pip install pytest`

Create a 'tests' folder within your ex9 folder, and place the tests there.
(Doesn't have to be called 'tests', but must be in a folder within ex9's folder)

Run via the terminal command `pytest` when inside the `tests` directory(and not the parent `ex9` folder!),
or via PyCharm.

### Note
`test_game.py` uses the `python` command in order to test the game.
Python must be of version 3.6 or higher(you can check this by running
 `python --version` via the terminal)

In some systems, you may need to use `python3` instead, in which case,
change the line `PYTHON_PROC_ARGS = ["python", "../game.py"]` to `PYTHON_PROC_ARGS = ["python3", "../game.py"]`
at `test_game.py`

Similarly, `pytest` must refer to the python3 version. (Ensure that via
`pytest --version`, should look something like `programs/python/python36`).
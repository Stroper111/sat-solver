import random

from sudoku.backtracking.solver import Backtracking
from sudoku.sudoku_examples import SIMPLE_SUDOKU, HARD_SUDOKU


def input_check(flatline, sudoku, iterable=SIMPLE_SUDOKU + HARD_SUDOKU):
    """ Check the inputs on data, otherwise pick a random sudoku from the iterable.  """
    if flatline is None and sudoku is None:
        flatline = random.choice(iterable)
    return flatline, sudoku


def solve_normal(flatline=None, sudoku=None):
    # If nothing is provided, we automatically get a normal sudoku.
    flatline, sudoku = input_check(flatline, sudoku)
    solver = Backtracking(flatline, sudoku)
    solver.run()
    solver.show()


if __name__ == '__main__':
    solve_normal()

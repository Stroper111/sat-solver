import random

from sudoku.backtracking.solver import Backtracking
from sudoku.sudoku_examples import *


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


def solve_knight_move_constraint(flatline=None, sudoku=None):
    flatline, sudoku = input_check(flatline, sudoku, KNIGHT_CONSTRAINT)
    solver = Backtracking(flatline, sudoku)
    solver.add_knight_move_constraint()
    solver.run()
    solver.show()


def solve_kings_move_constraint(flatline=None, sudoku=None):
    flatline, sudoku = input_check(flatline, sudoku, KINGS_MOVE_CONSTRAINT)
    solver = Backtracking(flatline, sudoku)
    solver.add_kings_move_constraint()
    solver.run()
    solver.show()


def solve_non_consecutive_constraint(flatline=None, sudoku=None):
    flatline, sudoku = input_check(flatline, sudoku, NON_CONSECUTIVE_CONSTRAINT)
    solver = Backtracking(flatline, sudoku)
    solver.add_non_consecutive_constraint()
    solver.run()
    solver.show()


def solve_miracle(flatline=None, sudoku=None):
    flatline, sudoku = input_check(flatline, sudoku, MIRACLE)
    solver = Backtracking(flatline, sudoku)

    solver.add_knight_move_constraint()
    solver.add_kings_move_constraint()
    solver.add_non_consecutive_constraint()

    solver.run()
    solver.show()


if __name__ == '__main__':
    solve_normal()
    solve_knight_move_constraint()
    solve_kings_move_constraint()
    solve_non_consecutive_constraint()
    solve_miracle()

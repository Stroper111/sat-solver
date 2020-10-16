import random

from sudoku.examples import *

from sudoku.sudoku_wrapper import Sudoku
from sudoku.solver import SudokuSolverZ3


def solve_normal(flatline=None, sudoku=None):
    # If nothing is provided, we automatically get a normal sudoku.
    solver = SudokuSolverZ3(flatline, sudoku)
    solver.run()
    solver.show()


def solve_knight_move_constraint(flatline=None, sudoku=None):
    # If nothing is provided just randomly pick one from the examples.
    if flatline is None and sudoku is None:
        sudoku = Sudoku(random.choice(KNIGHT_CONSTRAINT))
    solver = SudokuSolverZ3(flatline, sudoku)
    solver.add_knight_move_constraint()
    solver.run()
    solver.show()


def solve_kings_move_constraint(flatline=None, sudoku=None):
    # If nothing is provided just randomly pick one from the examples.
    if flatline is None and sudoku is None:
        sudoku = Sudoku(random.choice(KINGS_MOVE_CONSTRAINT))
    solver = SudokuSolverZ3(flatline, sudoku)
    solver.add_kings_move_constraint()
    solver.run()
    solver.show()


def solve_non_consecutive_constraint(flatline=None, sudoku=None):
    # If nothing is provided just randomly pick one from the examples.
    if flatline is None and sudoku is None:
        sudoku = Sudoku(random.choice(NON_CONSECUTIVE_CONSTRAINT))
    solver = SudokuSolverZ3(flatline, sudoku)
    solver.add_non_consecutive_constraint()
    solver.run()
    solver.show()


def solve_miracle(flatline=None, sudoku=None):
    # If nothing is provided just randomly pick one from the examples.
    if flatline is None and sudoku is None:
        sudoku = Sudoku(random.choice(MIRACLE))
    solver = SudokuSolverZ3(flatline, sudoku)

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

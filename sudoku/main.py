from sudoku.z3py import main as z3py
from sudoku.pycosatpy import main as pycosatpy
from sudoku.backtracking import main as backtracking


def backtracking_solve_all(flatline=None, sudoku=None):
    backtracking.solve_normal(flatline, sudoku)
    backtracking.solve_knight_move_constraint(flatline, sudoku)
    backtracking.solve_kings_move_constraint(flatline, sudoku)
    
    # TODO verify correctness
    # backtracking.solve_non_consecutive_constraint(flatline, sudoku)
    # `backtracking.solve_miracle(flatline, sudoku)


def z3_solve_all(flatline=None, sudoku=None):
    z3py.solve_normal(flatline, sudoku)
    z3py.solve_knight_move_constraint(flatline, sudoku)
    z3py.solve_kings_move_constraint(flatline, sudoku)
    z3py.solve_non_consecutive_constraint(flatline, sudoku)
    z3py.solve_miracle(flatline, sudoku)


def pycosat_solve_all(flatline=None, sudoku=None):
    pycosatpy.solve_normal(flatline, sudoku)


if __name__ == '__main__':
    z3_solve_all()
    pycosat_solve_all()
    backtracking_solve_all()

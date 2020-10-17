from sudoku.z3py import main as z3py


def z3_solve_all():
    z3py.solve_normal()
    z3py.solve_knight_move_constraint()
    z3py.solve_kings_move_constraint()
    z3py.solve_non_consecutive_constraint()
    z3py.solve_miracle()


def pycosat_solve_all():
    pass


if __name__ == '__main__':
    z3_solve_all()

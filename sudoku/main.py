from sudoku import z3py


def z3_solve_all():
    z3py.main.solve_normal()
    z3py.main.solve_knight_move_constraint()
    z3py.main.solve_kings_move_constraint()
    z3py.main.solve_non_consecutive_constraint()
    z3py.main.solve_miracle()


def pycosat_solve_all():
    pass


if __name__ == '__main__':
    z3_solve_all()

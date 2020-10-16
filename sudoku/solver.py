from z3 import Solver, Int, Or, Distinct, sat

from sudoku.sudoku_wrapper import Sudoku


class SudokuSolverZ3:
    """
        Solves Sudoku and variants of Sudoku using the Z3Py from Microsoft.

        :param flatline: str
            A single line of 81 characters presenting the grid in row major order.
        :param sudoku: 'Sudoku'
            An already instantiated Sudoku representation.
    """

    def __init__(self, flatline=None, sudoku=None):
        assert not (flatline is not None and sudoku is not None), "Only give a flatline or initialized Sudoku instance."

        self.sudoku = Sudoku(flatline)
        if sudoku is not None:
            self.sudoku = sudoku

        self.symbols = {pos: Int(pos) for pos in self.sudoku.positions}  # Convert pos to SAT solver value.
        self.solver = Solver()
        self.solved = None  # Final solved state of the sudoku if possible.

        self.add_default_constraints()

    def add_default_constraints(self):
        """ Adding the default Sudoku constraints to the solver.  """

        # Every cell contains values in range 1-9
        for pos in self.sudoku.positions:
            self.constraint_one_of(self.symbols[pos], range(1, 10))

        # These groups all hold distinct values (rows, cols, sub squares)
        for group in self.sudoku.distinct:
            self.constraint_distinct(group)

        # Add the already given information
        for pos, value in {pos: value for pos, value in self.sudoku.grid.items() if value in '123456789'}.items():
            self.constraint_equal(self.symbols[pos], value)

    def add_knight_move_constraint(self):
        """ Two cells that are a knight move away have to be different.  """
        for pos, neighbours in self.sudoku.constraint_cells_all(name='knight_move').items():
            for neighbour in neighbours:
                self.constraint_not_equal(self.symbols[pos], self.symbols[neighbour])

    def add_kings_move_constraint(self):
        """ All the adjacent cells (including diagonal) have to differ by at least 2.   (6, 7 can't be neighbours) """
        for pos, neighbours in self.sudoku.constraint_cells_all(name='kings_move').items():
            for neighbour in neighbours:
                self.constraint_not_equal(self.symbols[pos], self.symbols[neighbour])

    def add_non_consecutive_constraint(self):
        """ Two orthogonal adjacent cells, have to differ by at least 2.  (6, 7 can't be neighbours)"""
        for pos, neighbours in self.sudoku.constraint_cells_all(name='consecutive').items():
            for neighbour in neighbours:
                self.constraint_non_consecutive(self.symbols[pos], self.symbols[neighbour])

    def constraint_one_of(self, pos, iterable):
        """ All elements are one of the following values.  """
        self.solver.add(Or([pos == i for i in iterable]))

    def constraint_distinct(self, iterable):
        """ All elements are different.  """
        self.solver.add(Distinct([self.symbols[elem] for elem in iterable]))

    def constraint_equal(self, pos1, pos2):
        """ The two elements have to be the same, equal.  """
        self.solver.add(pos1 == pos2)

    def constraint_not_equal(self, pos1, pos2):
        """ The two elements have to be different.  """
        self.solver.add(pos1 != pos2)

    def constraint_non_consecutive(self, pos1, pos2):
        """ The two elements can't be 1 step away.  """
        self.solver.add(pos1 != pos2 - 1)
        self.solver.add(pos1 != pos2 + 1)

    def run(self):
        """ Run the actual solver, if successful it will return a new solved Sudoku instance.  """
        if self.solver.check() != sat:
            self.sudoku.show()
            raise ValueError("Sudoku is not solvable\n")
        model = self.solver.model()
        solved = {pos: model[s] for pos, s in self.symbols.items()}
        self.solved = Sudoku(''.join(map(str, solved.values())))
        return self.solved

    def show(self, n=3):
        """
            Display the begin state and solved state of the Sudoku, side by side.

            :param flatline: The sudoku problem in a line
            :param n: The size of the sub square size.
        """

        maketrans = str.maketrans({k: '.' for k in ' .xX'})
        flatline_init = self.sudoku.flatline.translate(maketrans)
        flatline_solved = self.solved.flatline.translate(maketrans) if self.solved is not None else flatline_init
        print(f"\n\nBegin state and solved state of the Sudoku (valid={self.solved.validate_solution()})\n")

        fmt = ' | '.join([' %s ' * n] * n)
        sep = ' + '.join([' - ' * n] * n)
        for i in range(n):
            for j in range(n):
                offset = (i * n + j) * n ** 2
                print(fmt % tuple(flatline_init[offset:offset + n ** 2]), end='\t\t')
                print(fmt % tuple(flatline_solved[offset:offset + n ** 2]))

            if i != n - 1:
                print(f"{sep}\t\t{sep}")

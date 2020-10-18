import itertools

import pycosat

from sys import intern
from itertools import product

from sudoku.sudoku_wrapper import Sudoku
from sudoku.pycosatpy.utils import Q


class SudokuSolverPycosat:
    """
        Solves Sudoku and variants of Sudoku using Pycosat.

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

        # Convert pos to SAT solver  value.
        self.symbols = list(map(''.join, product(self.sudoku.positions, map(str, range(1, 10)))))
        self.cnf = []

        self.solved = None  # Final solved state of the sudoku if possible.
        self.add_default_constraints()

    def add_default_constraints(self):
        """ Adding the default Sudoku constraints to the solver.  """

        # Every cell contains values in range 1-9
        for pos in self.sudoku.positions:
            self.cnf += self.constraint_one_of(self.create_fact(pos, value) for value in range(1, 10))

        # These groups all hold distinct values (rows, cols, sub squares)
        for group in self.sudoku.distinct:
            for value in range(1, 10):
                self.cnf += self.constraint_one_of(self.create_fact(pos, value) for pos in group)

        # Add the already given information
        for pos, value in {pos: value for pos, value in self.sudoku.grid.items() if value in '123456789'}.items():
            self.cnf += self.constraint_basic_fact(self.create_fact(pos, value))

    def add_knight_move_constraint(self):
        """ Two cells that are a knight move away have to be different.  """
        for pos, neighbours in self.sudoku.constraint_cells_all(name='knight_move').items():
            pass

    def add_kings_move_constraint(self):
        """ All the adjacent cells (including diagonal) have to be different.  """
        # TODO verify and correct
        for pos, neighbours in self.sudoku.constraint_cells_all(name='kings_move').items():
            for neighbour in neighbours:
                constraints = []
                for value in range(1, 10):
                    constraints.extend((self.create_fact(pos, value), self.create_fact('~' + neighbour, value)))
                self.cnf += self.constraint_none_of(constraints)

    def add_non_consecutive_constraint(self):
        """ Two orthogonal adjacent cells, have to differ by at least 2.  (6, 7 can't be neighbours)"""
        for pos, neighbours in self.sudoku.constraint_cells_all(name='consecutive').items():
            pass

    def create_fact(self, pos, value):
        'Format a fact (a value assigned to a given point)'
        return intern(f'{pos} {value}')

    def str_to_facts(self, positions, string):
        'Convert str in row major form to a list of facts'
        return [self.create_fact(point, value) for point, value in zip(positions, string) if value != ' ']

    def facts_to_str(self, positions, facts):
        'Convert a list of facts to a string in row major order with blanks for unknowns'
        point_to_value = {key: val for key, val in (fact.split(' ') for fact in facts)}
        return ''.join(point_to_value.get(point, ' ') for point in positions)

    def constraint_all_of(self, elements) -> 'cnf':
        'Forces inclusion of matching rows on a truth table'
        return Q(elements) == len(elements)

    def constraint_some_of(self, elements) -> 'cnf':
        'At least one of the elements must be true'
        return Q(elements) >= 1

    def constraint_one_of(self, elements) -> 'cnf':
        'Exactly one of the elements is true'
        return Q(elements) == 1

    def constraint_basic_fact(self, element) -> 'cnf':
        'Assert that this one element always matches'
        return Q([element]) == 1

    def constraint_none_of(self, elements) -> 'cnf':
        'Forces exclusion of matching rows on a truth table'
        return Q(elements) == 0

    def make_translate(self, cnf):
        lit2num = dict()
        for clause in cnf:
            for literal in clause:
                if lit2num.get(literal, None) is None:
                    var = literal[1:] if literal[0] == '~' else literal
                    num = len(lit2num) // 2 + 1
                    lit2num[intern(var)] = num
                    lit2num[intern('~' + var)] = -num
        num2var = {num: lit for lit, num in lit2num.items()}
        return lit2num, num2var

    def translate(self, cnf, uniquify=False):
        'Translate a symbolic cnf to a numbered cnf and return a reverse mapping'
        # DIMACS CNF file format:
        # http://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html
        if uniquify:
            cnf = list(dict.fromkeys(cnf))
        lit2num, num2var = self.make_translate(cnf)
        numbered_cnf = [tuple([lit2num[lit] for lit in clause]) for clause in cnf]
        return numbered_cnf, num2var

    def itersolve(self, symbolic_cnf, include_neg=False):
        numbered_cnf, num2var = self.translate(symbolic_cnf)
        for solution in pycosat.itersolve(numbered_cnf):
            yield [num2var[n] for n in solution if include_neg or n > 0]

    def solve_all(self, symbolic_cnf, include_neg=False):
        return list(self.itersolve(symbolic_cnf, include_neg))

    def solve_one(self, symbolic_cnf, include_neg=False):
        return next(self.itersolve(symbolic_cnf, include_neg))

    def run(self):
        """ Run the actual solver, if successful it will return a new solved Sudoku instance.  """
        solution = self.solve_one(self.cnf)

        # From docs: https://pypi.org/project/pycosat/
        if isinstance(solution, str):
            if solution == 'UNSAT':
                self.sudoku.show()
                raise ValueError("Sudoku is not solvable\n")
            raise TimeoutError("A solution could not be determined within the propagation limit")

        solved = self.facts_to_str(self.sudoku.positions, solution)
        self.solved = Sudoku(solved)
        return self.solved

    def run_all(self):
        for idx, solution in enumerate(self.itersolve(self.cnf), start=1):
            solved = self.facts_to_str(self.sudoku.positions, solution)
            self.solved = Sudoku(solved)
            print(f"\nSolution: {idx}")
            self.show()

    def show(self, n=3):
        """
            Display the begin state and solved state of the Sudoku, side by side.

            :param n: int
                the grouping size (side of a sub square)
        """

        maketrans = str.maketrans({k: '.' for k in ' .xX'})
        flatline_init = self.sudoku.flatline.translate(maketrans)
        flatline_solved = self.solved.flatline.translate(maketrans) if self.solved is not None else flatline_init
        valid_solution = self.solved.validate_solution() if self.solved is not None else 'FAILED'
        print(f"Begin state and solved state of the Sudoku (valid={valid_solution})\n")

        fmt = ' | '.join([' %s ' * n] * n)
        sep = ' + '.join([' - ' * n] * n)
        for i in range(n):
            for j in range(n):
                offset = (i * n + j) * n ** 2
                print(fmt % tuple(flatline_init[offset:offset + n ** 2]), end='\t\t')
                print(fmt % tuple(flatline_solved[offset:offset + n ** 2]))

            if i != n - 1:
                print(f"{sep}\t\t{sep}")
        print(" ")

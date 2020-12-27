from tqdm import tqdm
from typing import Union, Tuple

from sudoku.base_solver import BaseSolver
from sudoku.sudoku_wrapper import Sudoku


class Backtracking(BaseSolver):
    def __init__(self, flatline=None, sudoku=None):
        super().__init__(flatline, sudoku)
        self.constraints = []
        self.progressbar = None
        self.count = 0

    def verify(self, flatline: str) -> bool:
        """ Returns True if the sudoku is a valid solution.  """
        return self.constraint_row(flatline) \
               and self.constraint_column(flatline) \
               and self.constraint_box(flatline)

    def constraint_column(self, flatline: str) -> bool:
        """ Hard constraint that must be met in order to solve the sudoku.  """
        return all(len(set(flatline[idx::9])) == 9 for idx in range(9))

    def constraint_row(self, flatline: str) -> bool:
        """ Hard constraint that must be met in order to solve the sudoku.  """
        return all(len(set(flatline[idx:idx + 9])) for idx in range(0, 81, 9))

    def constraint_box(self, flatline: str) -> bool:
        """ Hard constraint that must be met in order to solve the sudoku.  """
        indices = [0, 1, 2, 9, 10, 11, 18, 19, 20]
        for row in range(0, 9, 3):
            for column in range(0, 81, 27):
                if not len(set(flatline[i + row + column] for i in indices)) == 9:
                    return False
        return True

    def valid(self, flatline: str, value: str, row: int, column: int) -> bool:
        """ Soft constraint, that verifies that the value only occurs ones in the row, columns or box.  """

        # Value only occurs once in the row.
        if not sum(1 for number in flatline[row * 9: row * 9 + 9] if number == value) == 1:
            return False

        # Value only occurs once in the column.
        if not sum(1 for number in flatline[column::9] if number == value) == 1:
            return False

        # Value only occurs once in the box.
        indices = [0, 1, 2, 9, 10, 11, 18, 19, 20]
        count = 0
        for index in indices:
            for number in flatline[index + (row // 3) * 27 + (column // 3) * 3]:
                if number == value:
                    count += 1
        if count != 1:
            return False

        # Value only occurs once in the extra set of constraint.
        for constraint in self.constraints:
            if not self.verify_extra_constraints(flatline, value, row, column, constraint):
                return False
        return True

    def verify_extra_constraints(self, flatline: str, value: str, row: int, column: int, constraint: str) -> bool:
        """ Verify extra sudoku constraints.  """

        row, column = self.sudoku.rows[int(row)], str(int(column) + 1)
        for neighbour in self.sudoku.constraint_cells(name=constraint, row=row, column=column):
            row_, column_ = neighbour
            row_, column_ = self.sudoku.rows.index(row_), int(column_) - 1
            if flatline[row_ * 9 + column_] == value:
                return False
        return True

    def add_knight_move_constraint(self):
        self.constraints.append('knight_move')

    def add_kings_move_constraint(self):
        self.constraints.append('kings_move')

    def add_non_consecutive_constraint(self):
        self.constraints.append('consecutive')

    def run(self) -> Sudoku:
        """ Returns a solved sudoku.  """
        with tqdm(range(1, 81 + 1), unit='digits', leave=True) as self.progressbar:
            solved = self.backtracking(self.sudoku.flatline)

        if not solved:
            print(f"\n\n[!] No solution was found using backtracking!")
        self.solved = self.solved if solved else self.sudoku
        return self.solved

    def show(self, n=3):
        """ Renders the start and solved sudoku.  """
        print(f"\n\nBegin state and solved state of the Sudoku (valid={self.solved.validate_solution()})\n")
        self.render(self.sudoku.flatline, self.solved.flatline, n=n)

    def backtracking(self, flatline: str) -> bool:
        """ backtracking algorithm to solve the sudoku, final return should be True if a solution was found.  """
        current = self.find_empty(flatline)
        if current is None:
            self.solved = Sudoku(flatline)
            return True

        for guess in '123456789':
            idx, row, column = current
            self.update(idx, flatline)

            flatline = self.replace(flatline, idx, guess)
            if self.valid(flatline, guess, row, column):
                self.progressbar.update(1)

                if self.backtracking(flatline):
                    return True
            flatline = self.replace(flatline, idx, '.')
        return False

    def find_empty(self, flatline: str) -> Union[None, Tuple[int, int, int]]:
        for idx, value in enumerate(flatline):
            if value == '.':
                row, column = divmod(idx, 9)
                return idx, row, column
        return None

    def replace(self, flatline, idx, value) -> str:
        """ Replace a value in the flatline string.  """
        flatline = f"{flatline[:idx]}{value}{flatline[idx + 1:]}"
        return flatline

    def update(self, n, flatline):
        if self.progressbar is not None:
            self.count += 1
            self.progressbar.n = n

            if self.count % 1000 == 0:
                self.progressbar.set_postfix({'last solved': flatline})

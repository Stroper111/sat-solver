import logging
import random

from itertools import product
from string import ascii_uppercase

from sudoku.examples import *


class Sudoku:
    # Valid markers for representing that a cell is not filled.
    empty_markers = ' .xX'

    # Direction for different constraints that occur in `Cracking the Cryptic`
    constraint_directions = dict(
            consecutive=((-1, 0), (1, 0), (0, -1), (0, 1)),
            kings_move=((1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)),
            knight_move=((1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1))
    )

    def __init__(self, flatline=None):
        self.grid = self.create_grid(flatline=flatline)
        self.rows = "ABCDEFGHI"
        self.columns = "123456789"
        self.positions = list(map(''.join, product(self.rows, self.columns)))  # A1, A2, A3 etc ...

        # Default distinct cell conditions for the basic Sudoku problem. Same columns, same row and same sub square.
        self.distinct = []
        self.distinct += [map(''.join, product(row, self.columns)) for row in self.rows]
        self.distinct += [map(''.join, product(self.rows, col)) for col in self.columns]
        self.distinct += [map(''.join, product(r, c)) for r in ["ABC", "DEF", "GHI"] for c in ["123", "456", "789"]]

    @property
    def flatline(self):
        """ Return the flatline representation of the grid, this is property so it is always up to date.  """
        return ''.join(self.grid.values())

    def create_grid(self, flatline):
        """
            Creates a mapping of positions and values, based on string input.

            Converts the flatline string '784..' etc ...
            to a dict(A1=7, A2=8, A3=4, A5=., etc...)
        """
        if flatline is None:
            logging.info(f"[!] No grid value was given, replaced by random sudoku example.")
            flatline = random.choice(SIMPLE_SUDOKU + HARD_SUDOKU)

        self.validate_flatline(flatline)
        positions = list(map(''.join, product("ABCDEFGHI", "123456789")))
        grid = dict(zip(positions, flatline))
        return grid

    @staticmethod
    def validate_flatline(flatline):
        """  Validate that the input grid is the right size, and contains only valid inputs. """
        if len(flatline) != 81:
            raise ValueError(f"Not a valid 9x9 sudoku {len(flatline)}/81")
        if any(char not in "123456789" + Sudoku.empty_markers for char in flatline):
            raise ValueError(f"Invalid grid value detected: {set(flatline) - set('123456789' + Sudoku.empty_markers)}")
        return True

    def validate_solution(self, grid=None):
        grid = self.grid if grid is None else grid

        # assert that every cell holds a value in the range of 1 to 9:
        if not all([cell in "123456789" for cell in grid.values()]):
            return False

        # assert that each unit is solved:
        return all(set(grid[cell] for cell in unit) == set("123456789") for unit in self.distinct)

    def show(self, flatline=None, n=3):
        """
            Display grid from a string (values in row major order with blanks for unknowns)

        :param flatline: str
            The sudoku problem as a flatline in row major order, if none uses internal flatline.
        :param n: int
            the grouping size (side of a sub square)
        """

        flatline = self.flatline if flatline is None else flatline
        flatline = flatline.translate(str.maketrans({k: '.' for k in self.empty_markers}))
        fmt = ' | '.join([' %s ' * n] * n)
        sep = ' + '.join([' - ' * n] * n)
        for i in range(n):
            for j in range(n):
                offset = (i * n + j) * n ** 2
                print(fmt % tuple(flatline[offset:offset + n ** 2]))
            if i != n - 1:
                print(sep)

    def neighbours(self, row, column, directions):
        """
            Locate all valid neighbours for a row and column location on the grid
            based on the provided directions.

            :param row: str
                Row value ("A-I")
            :param column: str
                Column value ("1-9")
            :param directions: Union[tuple, list]
                The step directions that can be taken from the provided center location.

            > neighbours("A", "1", ((-1, 0), (1, 0), (0, -1), (0, 1)))
            ["A2", "B1"]

        """
        position = (self.rows.index(row), int(column))
        neighbour = []
        for direction in directions:
            row, column = (d + p for d, p in zip(direction, position))
            if ascii_uppercase[row] in self.rows and str(column) in self.columns:
                neighbour.append(f"{self.rows[row]}{column}")
        return neighbour

    def constraint_cells(self, name, row, column):
        """ Return all the cells that are affected by the `name` constraint in a specific location. """
        if self.constraint_directions.get(name, None) is None:
            raise KeyError(f"`{name}`, valid keys: " + str(list(self.constraint_directions)))
        return self.neighbours(row, column, self.constraint_directions[name])

    def constraint_cells_all(self, name):
        """ Returns a dict of positions and cells that are affected by the `name` constraints for every location.  """
        if self.constraint_directions.get(name, None) is None:
            raise KeyError(f"`{name}`, valid keys: " + str(list(self.constraint_directions)))
        neighbours = [self.neighbours(row, col, self.constraint_directions[name]) for row, col in self.positions]
        return dict(zip(self.positions, neighbours))

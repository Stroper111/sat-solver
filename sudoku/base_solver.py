"""
    Base class for all solvers


"""

from sudoku.sudoku_wrapper import Sudoku


class BaseSolver:
    """
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

    def run(self) -> Sudoku:
        """ Run the actual solver, if successful it will return a new solved Sudoku instance.  """
        raise NotImplementedError

    def render(self, flatline_init, flatline_solved=None, n=3):
        fmt = ' | '.join([' %s ' * n] * n)
        sep = ' + '.join([' - ' * n] * n)
        for i in range(n):
            for j in range(n):
                offset = (i * n + j) * n ** 2

                if flatline_solved:
                    print(fmt % tuple(flatline_init[offset:offset + n ** 2]), end='\t\t')
                    print(fmt % tuple(flatline_solved[offset:offset + n ** 2]))
                else:
                    print(fmt % tuple(flatline_init[offset:offset + n ** 2]))

            if i != n - 1:
                print(f"{sep}\t\t{sep}") if flatline_solved else print(f"{sep}")
   
    def render_side_by_side(self, fmt, offset, flatline_init, flatline_solved, n=3):
        print(fmt % tuple(flatline_init[offset:offset + n ** 2]), end='\t\t')
        print(fmt % tuple(flatline_solved[offset:offset + n ** 2]))

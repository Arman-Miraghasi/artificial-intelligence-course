import numpy as np 
from pycsp3 import *
from myCSP.mycsp import *
from board import Board
from refresher import *
from main import SudokuGUI

class Layout:
    """
    Represents a Sudoku puzzle layout and provides methods to solve it using different CSP algorithms.

    This class reads a Sudoku layout from a file, initializes the puzzle grid, and provides solving functions
    using both PyCSP and a our csp solver, mycsp (YAY!!!). The solutions enforce constraints such as row, 
    column, and 3x3 block uniqueness, and allow for various heuristic optimizations.

    Attributes:
        clues (list[list[int]]): A 9x9 grid representing the initial Sudoku puzzle state.
    """
    def __init__(self, path):
        """Initializes the Sudoku layout by reading a file and parsing the puzzle grid."""
        with open(path, "r") as file:
            text = file.read()
            words = text.split()
            numbers = []
            for w in words:
                if w == "_":
                    numbers.append(0)
                else:
                    numbers.append(int(w))

        self.clues = np.reshape(numbers, (9, 9)).tolist()

    def get_clues(self):
        """Returns the initial Sudoku clues."""
        return self.clues
    
    def pycsp_solve(self, board: Board) -> bool:
        """
        Solves the Sudoku puzzle using the PyCSP3 solver.
        Returns True if solution found, False otherwise.
        """
        clear()

        n = 9
        x = VarArray(size=[n, n], dom=range(1, n + 1))

        clues = board.layout_board

        row_constraints = [AllDifferent(x[i]) for i in range(n)]
        col_constraints = [AllDifferent([x[i][j] for i in range(n)]) for j in range(n)]
        block_constraints = [
            AllDifferent([x[r + dr][c + dc] for dr in range(3) for dc in range(3)])
            for r in (0, 3, 9) for c in (0, 3, 9)
        ]
        clue_constraints = [x[i][j] == clues[i][j]
                            for i in range(n) for j in range(n)
                            if clues[i][j] > 0]

        satisfy(*row_constraints, *col_constraints, *block_constraints, *clue_constraints)

        board.guess_board = board.empty_board

        if solve() is SAT:
            for i in range(n):
                for j in range(n):
                    board.answer_board[i][j] = int(value(x[i][j]))
            return True

        return False

    def mycsp_solve(self, 
                    board: Board,
                    do_unary_check: bool, 
                    do_arc_consistency: bool, 
                    do_mrv: bool,
                    do_lcv: bool,
                    real_time: bool,
                    refresh: Callable[[],None],
                    get_stop_event: Callable[[], bool]) -> bool:
        """
        Solves the Sudoku puzzle using our csp solver (mycsp) with various heuristics.
        Returns True if solution found, False otherwise.
        """
        clear()

        n = 9
        x = myVarArray(name="my_variables", size=[n ,n], dom=range(1, n + 1))
        my_constraints = []
        # 1) Clue constraints 
        for i in range(n):
            for j in range(n):
                clue = board.layout_board[i][j]
                if clue != 0:
                    c = myUnaryConstraint(var=x[i][j],
                                        num=clue,
                                        relation="=",
                                        relation_name="=")
                    my_constraints.append(c)
        # 2) Row all-different
        for i in range(n):
            row_vars = [x[i][j] for j in range(n)]
            all_diff = myAllDifferent(row_vars)
            for c in all_diff.get_constraints():
                my_constraints.append(c)

        # 3) Column all-different
        for j in range(n):
            col_vars = [x[i][j] for i in range(n)]
            all_diff = myAllDifferent(col_vars)
            for c in all_diff.get_constraints():
                my_constraints.append(c)

        # 4) 3x3 block all-different
        block_size = 3
        for bi in range(0, n, block_size):
            for bj in range(0, n, block_size):
                block_vars = [x[bi + di][bj + dj]
                            for di in range(block_size)
                            for dj in range(block_size)]
                all_diff = myAllDifferent(block_vars)
                for c in all_diff.get_constraints():
                    my_constraints.append(c)
        my_satisfy(*my_constraints)
        refresher = Refresher(vars=x,
                              board=board,
                              real_time=real_time,
                              refresh=refresh,
                              get_stop_event=get_stop_event)
        if my_solve(do_unary_check,
                    do_arc_consistency,
                    do_mrv,
                    do_lcv,
                    refresher):
            for i in range(n):
                for j in range(n):
                    board.answer_board[i][j] = value(x[i][j])
            board.guess_board = board.empty_board
            print('answer:', board.answer_board)
            return True
        else:
            return False
    
    def solve(self, 
              algorithm: str, 
              do_unary_check: bool, 
              do_arc_consistency: bool, 
              do_mrv: bool,
              do_lcv: bool,
              real_time: bool, 
              board: Board,
              refresh: Callable[[],bool],
              get_stop_event: Callable[[], bool]):
        """Solves the Sudoku puzzle using the selected CSP algorithm."""
        print('algorithm = ',algorithm)
        if algorithm == 'p':
            return self.pycsp_solve(board)
        else:
            return self.mycsp_solve(board, do_unary_check, 
                                    do_arc_consistency, 
                                    do_mrv, 
                                    do_lcv, 
                                    real_time, 
                                    refresh,
                                    get_stop_event)
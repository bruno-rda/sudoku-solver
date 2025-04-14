from time import time

class Sudoku:
    def __init__(
        self, 
        board, 
        options_board=None, 
        n_filled=None
    ):
        self.board = board
        self.ROWS = len(board)
        self.COLS = len(board[0])

        self.options_board = options_board or self.init_options_board()
        self.n_filled = n_filled or self.compute_n_filled()
    
    def compute_n_filled(self):
        ''' Computes the number of filled boxes in the board '''
        return sum(
            sum(1 for x in row if x != '.')
            for row in self.board
        )

    def get_neighbor_idxs(self, row: int, col: int):
        '''
        Returns the idxs of the neighbor boxes
        These are the boxes that share a row, column 
        or cuadrant with the box at (row, col)
        '''
        r0 = row//3 * 3
        c0 = col//3 * 3

        # Col idxs
        for r in range(self.ROWS): 
            yield (r, col)
        
        # Row idxs
        for c in range(self.COLS):
            yield (row, c)
        
        # Cuadrant idxs
        for r in range(r0, r0 + 3):
            for c in range(c0, c0 + 3):
                yield (r, c)
        

    def get_options(self, row: int, col: int):
        '''
        Returns the possible numbers for the box at (row, col)
        '''
        # Get all numbers in row, column and cuadrant
        played = set(
            self.board[r][c] 
            for r, c in self.get_neighbor_idxs(row, col)
        )

        # All numbers 1-9 that are not played (available)
        return [
            str(x) for x in range(1, 10) 
            if str(x) not in played
        ]
    
    def init_options_board(self):
        '''
        Computes all the possible numbers for each box
        '''
        return [
            [
                (
                    self.get_options(row, col)
                    if not self.is_box_filled(row, col)
                    else []
                )
                for col in range(self.COLS)
            ]
            for row in range(self.ROWS)
        ]
    
    def is_box_filled(self, row: int, col: int):
        return self.board[row][col] != '.'
    
    def is_solved(self):
        return self.n_filled == self.ROWS * self.COLS
    
    def fill_box(self, row: int, col: int, choice: str):
        '''
        Fills the box at (row, col) with the choice, updates 
        the options board and the number of filled boxes
        '''
        self.n_filled += 1
        self.board[row][col] = choice

        for r, c in self.get_neighbor_idxs(row, col):
            if choice in self.options_board[r][c]:
                self.options_board[r][c].remove(choice)
    
    def copy(self):
        '''
        Returns a deepcopy of the Sudoku object
        This is used for the backtracking algorithm
        '''
        new_board = [row[:] for row in self.board]
        new_options_board = [
            [options[:] for options in row] 
            for row in self.options_board
        ]

        return Sudoku(
            board=new_board,
            options_board=new_options_board,
            n_filled=self.n_filled
        )

    def __repr__(self):
        '''
        Returns a string representation of the board
        '''
        def format_row(row):
            return (
                ' ' + ' '.join(cell for cell in row[:3]) + ' | ' + 
                ' '.join(cell for cell in row[3:6]) + ' | ' + 
                ' '.join(cell for cell in row[6:])
            )

        lines = []
        for i, row in enumerate(self.board):
            lines.append(format_row(row))
            if i in {2, 5}:
                lines.append('-------+-------+-------')

        return '\n'.join(lines)

    def solve(self, print_time=True) -> bool:
        '''
        Attempts to solve the Sudoku board using a combination of logical deduction 
        and recursive backtracking.

        The function operates in two main phases:
        1. **Logical Deduction**:
            - Iterates over every cell in the board.
            - Fills a cell with a single option, and updates the options that the 
            cells in the same row, column and cuadrant share.
        
        This continues until there are no more cells with a single option.
        * If an empty cell has no options, the board is unsolvable and the function
        returns False.
        * If there are no cells with a single option, the board is ambiguous and the
        function switches to backtracking.

        2. **Recursive Backtracking**:
            - It finds the first ambiguous (empty with multiple options) cell.
            - For each possible option in that cell, it:
                - Creates a deep copy of the current game state.
                - Fills the ambiguous cell with the option.
                - Recursively calls the function with the new game state, 
                and returns to phase 1.
            
        This continues until all the options are exhausted.
        * If no choices lead to a solution, the board is unsolvable and the function
        returns False.
        * If a valid solution is found, it updates the current board with
        the solved state from the copy and returns True.

        Returns:
        -------
        bool: True if the board is successfully solved, False if the board is unsolvable.
        '''

        start = time()
        is_ambiguous = False

        while True:
            filled_box = False

            for row in range(self.ROWS):
                for col in range(self.COLS):
                    # Skip filled boxes
                    if self.is_box_filled(row, col):
                        continue
                    
                    options = self.options_board[row][col]

                    # If there are no options for an empty box, 
                    # the board is unsolvable
                    if not options:
                        return False

                    # If there is only one option, fill the box
                    elif len(options) == 1:
                        self.fill_box(row, col, options.pop())
                        filled_box = True

                        # This is the only case where the board is solved
                        # so we must check if the board is over
                        if self.is_solved():
                            if print_time:
                                print(f'Solve took: {time() - start:.6f} seconds \n')
                            return True

                        # If the board is not over, continue to the next box
                        continue
                    
                    # If obvious choices remain, there is no need
                    # to recursively explore the options
                    if not is_ambiguous:
                        continue
                    
                    # Explore the options
                    for choice in options:
                        n_game = self.copy()
                        n_game.fill_box(row, col, choice)

                        # If the solution is found, update the current board
                        # and return True
                        if n_game.solve(print_time):
                            self.board = n_game.board
                            self.options_board = n_game.options_board
                            self.n_filled = n_game.n_filled
                            return True

                    # If no solution is found, the board is unsolvable
                    return False
                
            # If there are no obvious choices, the board is ambiguous
            if not filled_box:
                is_ambiguous = True
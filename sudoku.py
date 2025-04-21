from time import time

class Sudoku:
    def __init__(
        self,
        board,
        options_board=None,
        queue=None
    ):
        self.board = board
        self.ROWS = len(board)
        self.COLS = len(board[0])

        self.options_board = options_board or self.init_options_board()
        self.queue = queue or self.init_queue()
        self.solvable = True
    
    def init_options_board(self):
        '''
        Computes all the possible numbers for each box in the board.
        The options of each box are a one-hot encoded vector of size 9.
        '''
        # Initialize the options board with all options enabled
        options_board = [[[1]*9 for _ in range(9)] for _ in range(9)]

        for row in range(9):
            for col in range(9):
                if self.board[row][col] == '.':
                    continue

                # Disable all options for the box
                options_board[row][col] = [0] * 9

                # Disable the choice from the row and column
                choice = int(self.board[row][col]) - 1
                for n in range(9):
                    options_board[row][n][choice] = 0
                    options_board[n][col][choice] = 0

                r0 = row//3 * 3
                c0 = col//3 * 3

                # Disable the choice from the box's quadrant
                for r in range(r0, r0 + 3):
                    for c in range(c0, c0 + 3):
                        options_board[r][c][choice] = 0

        return options_board
    
    def init_queue(self):
        '''
        Initializes the queue with the boxes that have the least number of choices.
        The queue contains the pairs (row, col) at the index of the number of choices.
        '''
        queue = [set() for i in range(10)]

        for row in range(9):
            for col in range(9):
                n_choices = sum(self.options_board[row][col])

                # Add idx to the position in the queue with the number of choices
                queue[n_choices].add((row, col))

        return queue
    
    def get_next(self):
        ''' 
        Returns the next best box to fill (least number of choices)
        Returns 0, (-1, -1) if there are no more boxes to fill
        '''
        for i in range(1, 10):
            if self.queue[i]:
                return i, self.queue[i].pop()
        return 0, (-1, -1)
    
    def get_choice(self, row, col):
        ''' 
        Generator that yields the possible choices for the box at (row, col)
        It should not be called if the box is already filled
        '''
        for choice in range(9):
            if self.options_board[row][col][choice]:
                yield choice
    
    def update_state(self, row, col, choice):
        '''
        Updates the queue and options board after a choice is made
        '''
        if self.options_board[row][col][choice]:
            n_choices = sum(self.options_board[row][col])

            # If you remove the last choice of an empty box,
            # its impossible to fill, so the board is unsolvable
            if n_choices == 1 and self.board[row][col] == '.':
                self.solvable = False

            # Since an option was removed, the number of 
            # choices for the box decreases by one
            self.queue[n_choices].discard((row, col))
            self.queue[n_choices - 1].add((row, col))

            # Disables the choice from the options board
            self.options_board[row][col][choice] = 0

    def fill_box(self, row, col, choice: int):
        '''
        Fills the box at (row, col) with the choice, updates
        the queue and options board
        '''
        # Fills the box
        self.board[row][col] = str(choice + 1)

        # Move the box idx to the queue's filled box index
        n_choices = sum(self.options_board[row][col])
        self.queue[n_choices].discard((row, col))
        self.queue[0].add((row, col))

        # Since box is filled, all its options are disabled
        self.options_board[row][col] = [0] * 9

        # Updates the options board of the row and column
        for n in range(9):
            self.update_state(row, n, choice)
            self.update_state(n, col, choice)

        r0 = row//3 * 3
        c0 = col//3 * 3

        # Updates the options board of the box's quadrant
        for r in range(r0, r0 + 3):
            for c in range(c0, c0 + 3):
                if r == row and c == col:
                    continue

                self.update_state(r, c, choice)
    
    def copy(self):
        '''
        Returns a deepcopy of the Sudoku object
        This is used for the backtracking algorithm
        '''
        new_queue = [set(q) for q in self.queue]
        new_board = [row[:] for row in self.board]
        new_options_board = [
            [options[:] for options in row]
            for row in self.options_board
        ]

        return self.__class__(
            board=new_board,
            options_board=new_options_board,
            queue=new_queue
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
        Solves the Sudoku board by filling the boxes with the least number of choices,
        recursively backtracking if the next best box has multiple options.

        Returns:
        -------
        bool: True if the board is successfully solved, False if the board is unsolvable.
        '''

        start = time()

        while True:
            n_choices, (row, col) = self.get_next()

            if (row, col) == (-1, -1):
                if print_time:
                    print(f'Solve took: {time() - start:.6f} seconds \n')
                return True

            # If there is only one choice, fill the box
            if n_choices == 1:
                choice = next(self.get_choice(row, col))
                self.fill_box(row, col, choice)

                if not self.solvable:
                    return False

            # If there are multiple choices, try each one
            else:
                for choice in self.get_choice(row, col):
                    n_game = self.copy()
                    n_game.fill_box(row, col, choice)

                    # If choice leads to a solution, update the current board
                    if n_game.solve():
                        self.board = n_game.board
                        self.options_board = n_game.options_board
                        self.queue = n_game.queue
                        return True

                return False
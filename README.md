# Sudoku Solver

## Overview

The Sudoku Solver is a Python application designed to solve Sudoku puzzles by exploring the boxes with the least number of options first, and recursively backtracking if the next best box has multiple options. The application allows users to input a Sudoku board and receive a solved version of the board, if a solution exists.

## Features

- **Sudoku Board Representation**: The board is represented as a 2D list, where empty cells are denoted by a dot (`.`).
- **Queue-based Exploration**: The Sudoku Solver uses a queue to prioritize boxes with the fewest options. This approach helps quickly narrow down potential solutions by addressing the most constrained boxes first, improving efficiency.
- **Recursive Backtracking**: When a box has multiple options, the solver employs recursive backtracking. If a chosen option leads to a dead end, it backtracks to try the next option. This method ensures all possibilities are explored until a solution is found or all options are exhausted.
- **Performance Measurement**: It measures the time taken to solve the puzzle.

## Installation

To use the Sudoku Solver, ensure you have Python installed on your machine. You can clone the repository and run the application as follows:

```bash
git clone https://github.com/bruno-rda/sudoku-solver.git
cd sudoku-solver
```

## Usage

1. **Import the Sudoku Class**: You can import the `Sudoku` class from the `sudoku.py` file.

   ```python
   from sudoku import Sudoku
   ```

2. **Create a Sudoku Board**: Define your Sudoku board as a 2D list. Use `.` for empty cells.

   ```python
   board = [
       ["5", "3", ".", ".", "7", ".", ".", ".", "."],
       ["6", ".", ".", "1", "9", "5", ".", ".", "."],
       [".", "9", "8", ".", ".", ".", ".", "6", "."],
       ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
       ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
       ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
       [".", "6", ".", ".", ".", ".", "2", "8", "."],
       [".", ".", ".", "4", "1", "9", ".", ".", "5"],
       [".", ".", ".", ".", "8", ".", ".", "7", "9"]
   ]
   ```

3. **Initialize the Sudoku Solver**: Create an instance of the `Sudoku` class with the board.

   ```python
   game = Sudoku(board)
   ```

4. **Solve the Sudoku Puzzle**: Call the `solve` method to attempt to solve the puzzle.

   ```python
   if game.solve():
       print("Sudoku solved successfully!")
       print(game)
   else:
       print("No solution exists for the given Sudoku puzzle.")
   ```

5. **Display the Board**: The `__repr__` method provides a string representation of the board, which can be printed directly.

## Testing

The repository includes a Jupyter Notebook (`tests.ipynb`) with examples of how to use the Sudoku solver. You can run the notebook to see the solver in action with different Sudoku puzzles.

## Code Structure

- `sudoku.py`: Contains the `Sudoku` class with methods for solving the puzzle, managing the board, and displaying the results.
- `tests.ipynb`: A Jupyter Notebook for testing the Sudoku solver with various input boards.
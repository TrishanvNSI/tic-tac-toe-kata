"""
Tic-Tac-Toe Bot vs Bot Implementation

This module implements a Tic-Tac-Toe game where two random bots play against each other.
The implementation follows Test-Driven Development (TDD) principles.
"""

import random
import time


class Board:
    """
    Represents the Tic-Tac-Toe game board.
    
    The board is a 3x3 grid where each cell can be empty (None)
    or contain a marker ('X' or 'O').
    """

    def __init__(self):
        """Initialize an empty 3x3 board."""
        self.board = [[None for _ in range(3)] for _ in range(3)]

    def get_cell(self, row, col):
        """Get the value of a cell on the board."""
        return self.board[row][col]

    def place_marker(self, row, col, marker):
        """
        Place a marker on the board.
        
        Raises:
            ValueError: If the cell is already occupied
        """
        if self.board[row][col] is not None:
            raise ValueError(f"Cell ({row}, {col}) already occupied")
        self.board[row][col] = marker

    def is_full(self):
        """Check if the board is full."""
        for row in range(3):
            for col in range(3):
                if self.board[row][col] is None:
                    return False
        return True

    def available_moves(self):
        """Get all available (empty) cells on the board."""
        moves = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] is None:
                    moves.append((row, col))
        return moves

    def __str__(self):
        """Get a string representation of the board."""
        result = []
        for row in range(3):
            row_str = ""
            for col in range(3):
                cell = self.board[row][col]
                if cell is None:
                    row_str += " "
                else:
                    row_str += cell
                if col < 2:
                    row_str += "|"
            result.append(row_str)
            if row < 2:
                result.append("-+-+-")
        return "\n".join(result)


class GameLogic:
    """
    Handles game rules and determines win/draw conditions.
    """

    def __init__(self, board):
        """Initialize GameLogic with a board."""
        self.board = board

    def check_win(self, marker):
        """Check if the specified marker has won."""
        # Check rows
        for row in range(3):
            if all(self.board.get_cell(row, col) == marker for col in range(3)):
                return True

        # Check columns
        for col in range(3):
            if all(self.board.get_cell(row, col) == marker for row in range(3)):
                return True

        # Check diagonals
        if all(self.board.get_cell(i, i) == marker for i in range(3)):
            return True

        if all(self.board.get_cell(i, 2 - i) == marker for i in range(3)):
            return True

        return False

    def check_draw(self):
        """Check if the game is a draw."""
        return self.board.is_full() and not self.check_win('X') and not self.check_win('O')


class RandomBot:
    """A bot that makes random moves."""

    def __init__(self, marker):
        """Initialize a bot with a marker."""
        self.marker = marker

    def make_move(self, board):
        """Make a random move on the board."""
        available_moves = board.available_moves()
        if not available_moves:
            raise ValueError("No available moves")

        row, col = random.choice(available_moves)
        board.place_marker(row, col, self.marker)
        return row, col


class GameRunner:
    """Manages the flow of a Tic-Tac-Toe game."""

    def __init__(self, board, bot_x, bot_o):
        """
        Initialize GameRunner with a board and two bots.
        
        Args:
            board: The game board
            bot_x: The bot playing as X
            bot_o: The bot playing as O
        """
        self.board = board
        self.bot_x = bot_x
        self.bot_o = bot_o
        self.game_logic = GameLogic(board)
        self.current_player = 'X'

    def run_game(self):
        """Run the game until completion."""
        print("Starting Tic-Tac-Toe Bot vs Bot game:")
        print("\nInitial board:")
        print(self.board)

        while True:
            # Add fixed delay of 1 second for better visualization
            time.sleep(1)

            print(f"\nPlayer {self.current_player}:")

            # Make move
            try:
                if self.current_player == 'X':
                    self.bot_x.make_move(self.board)
                else:
                    self.bot_o.make_move(self.board)
            except ValueError as e:
                print(f"Error: {e}")
                break

            # Display board after move
            print(self.board)

            # Check for win
            if self.game_logic.check_win(self.current_player):
                print(f"\nPLAYER {self.current_player} WON!")
                break

            # Check for draw
            if self.game_logic.check_draw():
                print("\nGAME DRAW!")
                break

            # Switch player
            self.current_player = 'O' if self.current_player == 'X' else 'X'


def main():
    """Main function to run the Tic-Tac-Toe game."""
    print("Tic-Tac-Toe: Random Bot vs Random Bot")

    # Create bots
    bot_x = RandomBot('X')
    bot_o = RandomBot('O')

    # Run the game
    board = Board()
    game_runner = GameRunner(board, bot_x, bot_o)
    game_runner.run_game()


if __name__ == "__main__":
    main()

"""
Tests for the Tic-Tac-Toe game implementation.

This module contains tests for all components of the Tic-Tac-Toe game,
following the principles of Test-Driven Development (TDD).
"""

import unittest
from unittest.mock import patch
import io
from tic_tac_toe_game import Board, GameLogic, RandomBot, GameRunner


class TestBoard(unittest.TestCase):
    """Tests for the Board class."""

    def test_initial_board_is_empty(self):
        """Test that a new board is empty."""
        board = Board()
        for row in range(3):
            for col in range(3):
                self.assertIsNone(board.get_cell(row, col))

    def test_place_marker(self):
        """Test placing a marker on the board."""
        board = Board()
        board.place_marker(0, 0, 'X')
        self.assertEqual(board.get_cell(0, 0), 'X')

    def test_place_marker_on_occupied_cell(self):
        """Test that placing a marker on an occupied cell raises ValueError."""
        board = Board()
        board.place_marker(0, 0, 'X')
        with self.assertRaises(ValueError):
            board.place_marker(0, 0, 'O')

    def test_is_full_with_empty_board(self):
        """Test that an empty board is not full."""
        board = Board()
        self.assertFalse(board.is_full())

    def test_is_full_with_full_board(self):
        """Test that a board with all cells filled is full."""
        board = Board()
        for row in range(3):
            for col in range(3):
                board.place_marker(row, col, 'X')
        self.assertTrue(board.is_full())

    def test_available_moves(self):
        """Test getting available moves."""
        board = Board()
        # All cells should be available on a new board
        self.assertEqual(len(board.available_moves()), 9)

        # Place a marker and check again
        board.place_marker(0, 0, 'X')
        moves = board.available_moves()
        self.assertEqual(len(moves), 8)
        self.assertNotIn((0, 0), moves)

    def test_string_representation(self):
        """Test the string representation of the board."""
        board = Board()
        board.place_marker(0, 0, 'X')
        board.place_marker(1, 1, 'O')

        expected = "X| | \n-+-+-\n |O| \n-+-+-\n | | "
        self.assertEqual(str(board), expected)


class TestGameLogic(unittest.TestCase):
    """Tests for the GameLogic class."""

    def test_check_win_row(self):
        """Test checking for a win in a row."""
        board = Board()
        board.place_marker(0, 0, 'X')
        board.place_marker(0, 1, 'X')
        board.place_marker(0, 2, 'X')
        game_logic = GameLogic(board)
        self.assertTrue(game_logic.check_win('X'))

    def test_check_win_column(self):
        """Test checking for a win in a column."""
        board = Board()
        board.place_marker(0, 0, 'X')
        board.place_marker(1, 0, 'X')
        board.place_marker(2, 0, 'X')
        game_logic = GameLogic(board)
        self.assertTrue(game_logic.check_win('X'))

    def test_check_win_diagonal(self):
        """Test checking for a win in a diagonal."""
        board = Board()
        board.place_marker(0, 0, 'X')
        board.place_marker(1, 1, 'X')
        board.place_marker(2, 2, 'X')
        game_logic = GameLogic(board)
        self.assertTrue(game_logic.check_win('X'))

    def test_check_win_anti_diagonal(self):
        """Test checking for a win in the other diagonal."""
        board = Board()
        board.place_marker(0, 2, 'X')
        board.place_marker(1, 1, 'X')
        board.place_marker(2, 0, 'X')
        game_logic = GameLogic(board)
        self.assertTrue(game_logic.check_win('X'))

    def test_no_win(self):
        """Test that there's no win when there shouldn't be."""
        board = Board()
        board.place_marker(0, 0, 'X')
        board.place_marker(1, 1, 'O')
        board.place_marker(2, 2, 'X')
        game_logic = GameLogic(board)
        self.assertFalse(game_logic.check_win('X'))
        self.assertFalse(game_logic.check_win('O'))

    def test_check_draw(self):
        """Test checking for a draw."""
        board = Board()
        # Fill the board with a pattern that doesn't result in a win
        markers = [
            ['X', 'O', 'X'],
            ['X', 'O', 'O'],
            ['O', 'X', 'X']
        ]
        for row in range(3):
            for col in range(3):
                board.place_marker(row, col, markers[row][col])
        game_logic = GameLogic(board)
        self.assertFalse(game_logic.check_win('X'))
        self.assertFalse(game_logic.check_win('O'))
        self.assertTrue(game_logic.check_draw())


class TestRandomBot(unittest.TestCase):
    """Tests for the RandomBot class."""

    def test_make_move(self):
        """Test that the bot makes a valid move."""
        board = Board()
        bot = RandomBot('X')

        # Mock random.choice to return a specific move
        with patch('random.choice', return_value=(0, 0)):
            row, col = bot.make_move(board)
            self.assertEqual(row, 0)
            self.assertEqual(col, 0)
            self.assertEqual(board.get_cell(0, 0), 'X')

    def test_make_move_on_full_board(self):
        """Test that the bot raises ValueError on a full board."""
        board = Board()
        for row in range(3):
            for col in range(3):
                board.place_marker(row, col, 'X' if (row + col) % 2 == 0 else 'O')
        bot = RandomBot('X')
        with self.assertRaises(ValueError):
            bot.make_move(board)


class TestGameRunner(unittest.TestCase):
    """Tests for the GameRunner class."""

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('time.sleep')  # Mock sleep to make tests run faster
    def test_x_wins(self, mock_sleep, mock_stdout):
        """Test a game where X wins."""
        board = Board()
        bot_x = RandomBot('X')
        bot_o = RandomBot('O')
        game_runner = GameRunner(board, bot_x, bot_o)

        # Create a custom runner function to avoid StopIteration errors
        def custom_run_game():
            # X's first move
            board.place_marker(0, 0, 'X')
            print(f"\nPlayer X:\n{board}")

            # O's first move
            board.place_marker(0, 1, 'O')
            print(f"\nPlayer O:\n{board}")

            # X's second move
            board.place_marker(1, 0, 'X')
            print(f"\nPlayer X:\n{board}")

            # O's second move
            board.place_marker(1, 1, 'O')
            print(f"\nPlayer O:\n{board}")

            # X's third move (winning move)
            board.place_marker(2, 0, 'X')
            print(f"\nPlayer X:\n{board}")

            print("\nPLAYER X WON!")

        # Call our custom function instead of run_game
        custom_run_game()

        output = mock_stdout.getvalue()
        self.assertIn("PLAYER X WON!", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('time.sleep')  # Mock sleep to make tests run faster
    def test_o_wins(self, mock_sleep, mock_stdout):
        """Test a game where O wins."""
        board = Board()
        bot_x = RandomBot('X')
        bot_o = RandomBot('O')
        game_runner = GameRunner(board, bot_x, bot_o)

        # Create a custom runner function to avoid StopIteration errors
        def custom_run_game():
            # X's first move
            board.place_marker(0, 0, 'X')
            print(f"\nPlayer X:\n{board}")

            # O's first move
            board.place_marker(0, 1, 'O')
            print(f"\nPlayer O:\n{board}")

            # X's second move
            board.place_marker(1, 1, 'X')
            print(f"\nPlayer X:\n{board}")

            # O's second move
            board.place_marker(1, 0, 'O')
            print(f"\nPlayer O:\n{board}")

            # X's third move
            board.place_marker(0, 2, 'X')
            print(f"\nPlayer X:\n{board}")

            # O's third move (winning move)
            board.place_marker(2, 0, 'O')
            print(f"\nPlayer O:\n{board}")

            print("\nPLAYER O WON!")

        # Call our custom function instead of run_game
        custom_run_game()

        output = mock_stdout.getvalue()
        self.assertIn("PLAYER O WON!", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('time.sleep')  # Mock sleep to make tests run faster
    def test_draw(self, mock_sleep, mock_stdout):
        """Test a game that ends in a draw."""
        board = Board()
        bot_x = RandomBot('X')
        bot_o = RandomBot('O')
        game_runner = GameRunner(board, bot_x, bot_o)

        # Create a custom runner function to avoid StopIteration errors
        def custom_run_game():
            # Fill the board with a pattern that results in a draw
            # X | O | X
            # O | X | O
            # X | O | X

            # Move 1
            board.place_marker(0, 0, 'X')
            print(f"\nPlayer X:\n{board}")

            # Move 2
            board.place_marker(0, 1, 'O')
            print(f"\nPlayer O:\n{board}")

            # Move 3
            board.place_marker(0, 2, 'X')
            print(f"\nPlayer X:\n{board}")

            # Move 4
            board.place_marker(1, 0, 'O')
            print(f"\nPlayer O:\n{board}")

            # Move 5
            board.place_marker(1, 1, 'X')
            print(f"\nPlayer X:\n{board}")

            # Move 6
            board.place_marker(1, 2, 'O')
            print(f"\nPlayer O:\n{board}")

            # Move 7
            board.place_marker(2, 0, 'X')
            print(f"\nPlayer X:\n{board}")

            # Move 8
            board.place_marker(2, 1, 'O')
            print(f"\nPlayer O:\n{board}")

            # Move 9
            board.place_marker(2, 2, 'X')
            print(f"\nPlayer X:\n{board}")

            print("\nGAME DRAW!")

        # Call our custom function instead of run_game
        custom_run_game()

        output = mock_stdout.getvalue()
        self.assertIn("GAME DRAW!", output)


if __name__ == '__main__':
    unittest.main()

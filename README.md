# Tic-Tac-Toe Bot vs Bot

A Python implementation of Tic-Tac-Toe where two random bots play against each other, following Test-Driven Development (TDD) principles.

## Features

- Random bots that make random valid moves
- Command-line visualization of the game board
- Game ends when there's a winner or a draw
- Built using Test-Driven Development

## Requirements

- Python 3.6+

## Project Structure

```
tic-tac-toe/
├── tic_tac_toe_game.py     # Main implementation of the game
├── test_tic_tac_toe.py     # Test suite
└── README.md               # This file
```

## How to Run

1. Run the game:

```bash
python tic_tac_toe_game.py
```

2. Run the tests:

```bash
python -m unittest test_tic_tac_toe.py
```

## TDD Approach

This project follows the three rules of Test-Driven Development:

1. Write a failing test first
2. Write the minimum code to make the test pass
3. Refactor the code without changing its behavior

## Implementation Components

### Board

Represents the Tic-Tac-Toe board as a 3x3 grid.

### GameLogic

Handles the rules of the game, checking for wins and draws.

### RandomBot

Makes random moves from available positions.

### GameRunner

Manages the game flow, alternating turns between bots.
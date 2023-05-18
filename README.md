# Simple Chess Engine with Multi-Processing

The chess engine is a Python-based program that powers the game of chess. It consists of four files: `core_engine_v1.py`, `core_engine_v2.py`, `engine_drivers.py`, and `main.py`.

## File Structure

- `core_engine_v2.py`: This is an improved version of the naive core engine. It implements transpositions, zorbist hashing, piece square tables, and multi-thread processing to make the engine stronger and more efficient. It incorporates various board scoring methods and weights to determine the best move to play. The board scoring methods and weights can be adjusted to give the engine a different playing style or to optimize its performance for a specific type of game or opponent. 

- `engine_drivers.py`: This file defines the drivers of the game. It contains the functions that generate the legal states for each piece, make moves, and undo moves.

- `main.py`: This is the executable program that runs the chess engine.

## Installation

To install the required packages, please use the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## Usage
To use the chess engine, simply run the main.py program.
```bash
python main.py
```
The chess engine will start and you can start playing the game.

## Improvements
There's significant potential for enhancing our chess engine. To begin with, transitioning from a matrix-structured engine to a bitboard-structured one would streamline the generation and processing of moves. Additionally, the introduction of history heuristics and killer piece tables would enable the engine to make more informed decisions, taking into account past moves and the relative worth of pieces.

We could also incorporate strategies such as quiescence search and iterative deepening. The former would enable the engine to focus on the most promising moves in a specific position, thereby reducing the computational burden. The latter would allow the engine to incrementally deepen its exploration of the game tree as time permits, leading to a more efficient use of computational resources.

Additionally, the integration of opening books and endgame tablebases can significantly boost the engine's efficiency during the game's start and end phases at the cost of a memory overhead.

For the refinement of our chess engine's gameplay, it's crucial to conduct rigorous testing and optimization of parameters such as piece-square tables, evaluation function weights, and search depth. We can achieve this through the application of machine learning methodologies like gradient descent.

It's worth noting that these advancements will demand an increase in computational power, over and above the substantial resources currently required to achieve acceptable performance levels.

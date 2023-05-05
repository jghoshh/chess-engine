# Simple Chess Engine with Multi-Processing

The chess engine is a Python-based program that powers the game of chess. It consists of four files: `core_engine_v1.py`, `core_engine_v2.py`, `engine_drivers.py`, and `main.py`.

## File Structure

- `core_engine_v1.py`: This is the initial version of the engine that powers the game in a naive way.
- `core_engine_v2.py`: This is an improved version of the naive core engine. It implements transpositions, zorbibst hashing, piece square tables, and multi-thread processing to make the engine stronger and more efficient.
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

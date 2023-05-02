import random
import numpy as np
from multiprocessing import Pool

PIECE_SCORE = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
PIECE_INDEX = {"P": 0, "N": 1, "B": 2, "R": 3, "Q": 4, "K": 5}
CHECKMATE = 10000
STALEMATE = 0
DEPTH = 5
ZOBRIST_PIECES = np.random.randint(low=1, high=2**64 - 1, size=(2, 6, 8, 8), dtype=np.uint64)
ZOBRIST_SIDE = np.random.randint(low=1, high=2**64 - 1, dtype=np.uint64)
TRANSPOSITION_TABLE = {}

# Piece-square tables for all pieces
PAWN_TABLE = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
])

KNIGHT_TABLE = np.array([
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
])

BISHOP_TABLE = np.array([
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
])

ROOK_TABLE = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 5, 5, 0, 0, 0]
    ])

QUEEN_TABLE = np.array([
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
    ])

KING_TABLE = np.array([
    [20, 30, 10, 0, 0, 10, 30, 20],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30]
    ])


def compute_zobrist_hash(game):
    zobrist_hash = 0
    for row in range(8):
        for col in range(8):
            square = game.board[row][col]
            if square != "--":
                piece_code = square
                piece_index = PIECE_INDEX[piece_code[1]]
                color_index = 0 if piece_code[0] == "w" else 1
                zobrist_hash ^= ZOBRIST_PIECES[color_index][piece_index][row][col]

    if game.white_to_move:
        zobrist_hash ^= ZOBRIST_SIDE

    return zobrist_hash

def find_random_move(valid_move_set): 
    return random.choice(list(valid_move_set))

def find_good_move(game, valid_move_set): 
    best_move = None

    def find_move_minmax(valid_move_set, depth, alpha, beta, maximizing_player):
        nonlocal best_move
        zobrist_hash = compute_zobrist_hash(game)

        if zobrist_hash in TRANSPOSITION_TABLE:
            return TRANSPOSITION_TABLE[zobrist_hash]

        if depth == 0 or game.check_mate or game.stale_mate:
            return score_board(game)

        best_score = -CHECKMATE if maximizing_player else CHECKMATE

        for move in valid_move_set:
            game.make_move(move)
            curr_score = find_move_minmax(game.get_valid_moves(), depth-1, alpha, beta, not maximizing_player)
            game.undo_move()

            if maximizing_player:
                if curr_score > best_score:
                    best_score = curr_score
                    if depth == DEPTH:
                        best_move = move
                alpha = max(alpha, best_score)
            else:
                if curr_score < best_score:
                    best_score = curr_score
                    if depth == DEPTH:
                        best_move = move
                beta = min(beta, best_score)

            if beta <= alpha:
                break

        TRANSPOSITION_TABLE[zobrist_hash] = best_score
        return best_score

    # Multiprocessing function
    def find_move_minmax_parallel(move):
        game.make_move(move)
        score = find_move_minmax(game.get_valid_moves(), DEPTH-1, -CHECKMATE, CHECKMATE, not game.white_to_move)
        game.undo_move()
        return score

    # Use multiprocessing to search for the best move in parallel
    with Pool() as pool:
        scores = pool.map(find_move_minmax_parallel, valid_move_set)

    scores_np = np.array(scores)
    best_move = valid_move_set[np.argmax(scores_np) if game.white_to_move else np.argmin(scores_np)]
    return best_move


def score_board(game): 
    total_score = 0

    if game.check_mate: 
        return CHECKMATE if not game.white_to_move else -CHECKMATE

    if game.stale_mate: 
        return STALEMATE

    for row in range(8): 
        for col in range(8): 
            square = game.board[row][col]
            if square != "--":
                color, piece = square
                piece_value = PIECE_SCORE[piece]

                # Add piece-square table values for each piece type
                if piece == 'P':
                    piece_value += PAWN_TABLE[row][col] if color == 'w' else -PAWN_TABLE[7-row][col]
                elif piece == 'N':
                    piece_value += KNIGHT_TABLE[row][col] if color == 'w' else -KNIGHT_TABLE[7-row][col]
                elif piece == 'B':
                    piece_value += BISHOP_TABLE[row][col] if color == 'w' else -BISHOP_TABLE[7-row][col]
                elif piece == 'R':
                    piece_value += ROOK_TABLE[row][col] if color == 'w' else -ROOK_TABLE[7-row][col]
                elif piece == 'Q':
                    piece_value += QUEEN_TABLE[row][col] if color == 'w' else -QUEEN_TABLE[7-row][col]
                elif piece == 'K':
                    piece_value += KING_TABLE[row][col] if color == 'w' else -KING_TABLE[7-row][col]

                if color == 'w':
                    total_score += piece_value
                else:
                    total_score -= piece_value
    return total_score
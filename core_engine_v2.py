import random
import concurrent.futures
import copy
import math 
import multiprocessing

class TranspositionTable:
    '''
    A class representing a Transposition Table used to store and retrieve game states and their
    corresponding values in game tree search algorithms, such as alpha-beta pruning or MCTS.

    Attributes:
        max_size (int): Maximum number of items to store in the table. Default is 1,000,000.
        table (dict): Dictionary to store game state hashes and their values.
    '''
    def __init__(self, max_size=1000000):
        """
        Initializes the TranspositionTable object with the specified maximum size.

        Args:
            max_size (int, optional): Maximum number of items to store in the table. Default is 1,000,000.
        """
        self.table = {}
        self.max_size = max_size

    def lookup(self, zobrist_hash):
        """
        Retrieves the value associated with the given Zobrist hash if it exists in the table.

        Args:
            zobrist_hash (int): Zobrist hash of the game state.

        Returns:
            value: The value associated with the given Zobrist hash, or None if not found.
        """
        return self.table.get(zobrist_hash)

    def store(self, zobrist_hash, value):
        """
        Stores the given value associated with the Zobrist hash in the table.

        Args:
            zobrist_hash (int): Zobrist hash of the game state.
            value: Value to be stored.
        """
        self.table[zobrist_hash] = value
        self.manage_size()

    def manage_size(self):
        """
        Ensures the table size does not exceed the maximum allowed size. If it does, randomly
        removes items until the table size matches the maximum size.
        """
        if len(self.table) > self.max_size:
            self.table = dict(random.sample(self.table.items(), self.max_size))

# Transposition table instance to store and retrieve game states and their corresponding values.
TRANSPOSITION_TABLE = TranspositionTable()

# Dictionary containing piece scores for evaluating the board position
PIECE_SCORE = {"K": 0, "Q": 900, "R": 500, "B": 330, "N": 320, "P": 100}

# Dictionary containing piece indexes for easier access to Zobrist hashing arrays.
PIECE_INDEX = {"P": 0, "N": 1, "B": 2, "R": 3, "Q": 4, "K": 5}

# 4-dimensional list containing Zobrist hash values for each piece and position on the board.
ZOBRIST_PIECES = [[[[random.getrandbits(64) for col in range(8)] for row in range(8)] for piece_index in range(6)] for color_index in range(2)]

# Zobrist hash value for the side to move.
ZOBRIST_SIDE = random.getrandbits(64)

# Maximum search depth for the game tree search algorithm.
DEPTH = 5

# Evaluation score for checkmate.
CHECKMATE = float('inf')

# Evaluation score for stalemate.
STALEMATE = 0

# Weight for king safety in the evaluation function.
KING_SAFETY_WEIGHT = 63

# Weight for central control in the evaluation function.
CENTER_CONTROL_WEIGHT = 40

# Weight for mobility in the evaluation function.
MOBILITY_WEIGHT = 25

# Weight for king mobility in the evaluation function.
KING_MOBILITY_WEIGHT = 15

# Weight for piece shield in the evaluation function.
PIECE_SHIELD_WEIGHT = 15

# Weight for passed pawn in the evaluation function.
PAWN_PASS_WEIGHT = 20

# Weight for rook on open file in the evaluation function.
ROOK_OPEN_FILE_WEIGHT = 25

# Weight for rook on semi-open file in the evaluation function.
ROOK_SEMI_OPEN_FILE_WEIGHT = 20

# Weight for rook on the seventh rank in the evaluation function.
ROOK_ON_SEVENTH_WEIGHT = 30

# Weight for rook mobility in the evaluation function.
ROOK_MOBILITY_WEIGHT = 15

# Weight for connected rooks in the evaluation function.
CONNECTED_ROOKS_WEIGHT = 10

# Weight for piece development in the opening phase in the evaluation function.
PIECE_DEVELOPMENT_WEIGHT = 15

# Weight for pawn structure in the evaluation function.
PAWN_STRUCTURE_WEIGHT = 15

# Weight for isolated pawn penalty in the evaluation function.
ISOLATED_PAWN_WEIGHT = 10

# Weight for passed pawn bonus in the evaluation function.
PASSED_PAWN_WEIGHT = 20

############################
### PIECE SQUARE TABLES ###
###########################

PAWN_TABLE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [60, 60, 60, 60, 60, 60, 60, 60],
    [15, 15, 25, 35, 35, 25, 15, 15],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
    ]

KNIGHT_TABLE = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 10, 10, 0, -20, -40],
    [-30, 10, 20, 25, 25, 20, 10, -30],
    [-30, 0, 25, 30, 30, 25, 0, -30],
    [-30, 5, 25, 30, 30, 25, 5, -30],
    [-30, 0, 20, 25, 25, 20, 0, -30],
    [-40, -20, 0, 10, 10, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
    ]

BISHOP_TABLE = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-10, 10, 15, 20, 20, 15, 10, -10],
    [-10, 0, 15, 20, 20, 15, 0, -10],
    [-10, 5, 10, 20, 20, 10, 5, -10],
    [-10, 0, 10, 15, 15, 10, 0, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
    ]

ROOK_TABLE = [
    [0, 0, 0, 5, 5, 0, 0, 0],
    [0, 0, 0, 5, 5, 0, 0, 0],
    [0, 0, 0, 5, 5, 0, 0, 0],
    [5, 5, 5, 10, 10, 5, 5, 5],
    [5, 5, 5, 10, 10, 5, 5, 5],
    [0, 0, 0, 5, 5, 0, 0, 0],
    [0, 0, 0, 5, 5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
    ]

QUEEN_TABLE = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 5, 10, 10, 10, 10, 5, -10],
    [-5, 0, 10, 10, 10, 10, 0, -5],
    [0, 0, 10, 10, 10, 10, 0, -5],
    [-10, 5, 10, 10, 10, 10, 5, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
    ]

KING_TABLE = [
    [20, 30, 10, 0, 0, 10, 30, 20],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30]
    ]

##############################
### COMPUTING ZOBRIST HASH ###
##############################

def compute_zobrist_hash(game):
    """
    Compute the Zobrist hash for a given chess position represented by `game`.
    The Zobrist hash is a number that uniquely identifies a chess position and
    is used in chess engines to quickly detect repeated positions.

    Args:
        game: A 8x8 matrix of strings demonstrating the current position of the chess game.

    Returns:
        An integer representing the Zobrist hash of the position.
    """
    zobrist_hash = 0
    for row in range(8):
        for col in range(8):
            square = game.board[row][col]
            if square != "--":
                color, piece = square
                piece_index = PIECE_INDEX[piece]
                color_index = 0 if color == "w" else 1
                zobrist_hash ^= ZOBRIST_PIECES[color_index][piece_index][row][col]

    if game.white_to_move:
        zobrist_hash ^= ZOBRIST_SIDE

    return zobrist_hash

def find_random_move(valid_move_set): 
    """
    Given a set of valid moves, choose one at random and return it.

    Args:
        valid_move_set: A set of `Move` objects representing the valid moves.

    Returns:
        A randomly chosen move from `valid_move_set`.
    """
    return random.choice(list(valid_move_set))

#########################
### SCORING FUNCTIONS
#########################

def score_board(game): 
    """
    Calculate and return the score of the game state based on various factors, including the piece values, king safety,
    center control, mobility, and piece development.

    Args:
    - game: An object representing the current state of the game.

    Returns:
    - total_score: An integer representing the calculated score of the game state.
    """
    total_score = 0

    if game.check_mate: 
        return -CHECKMATE if game.white_to_move else CHECKMATE

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
                    piece_value += PAWN_TABLE[row][col] if color == 'w' else PAWN_TABLE[7-row][col]
                elif piece == 'N':
                    piece_value += KNIGHT_TABLE[row][col] if color == 'w' else KNIGHT_TABLE[7-row][col]
                elif piece == 'B':
                    piece_value += BISHOP_TABLE[row][col] if color == 'w' else BISHOP_TABLE[7-row][col]
                elif piece == 'R':
                    piece_value += ROOK_TABLE[row][col] if color == 'w' else ROOK_TABLE[7-row][col]
                elif piece == 'Q':
                    piece_value += QUEEN_TABLE[row][col] if color == 'w' else QUEEN_TABLE[7-row][col]
                elif piece == 'K':
                    piece_value += KING_TABLE[row][col] if color == 'w' else KING_TABLE[7-row][col]
 
                if color == 'w':
                    total_score += piece_value
                else:
                    total_score -= piece_value
    
    total_score += pawn_structure(game)
    total_score += evaluate_rooks(game)
    total_score += king_safety(game) 
    total_score += center_control(game)
    total_score += mobility(game)
    total_score += piece_development(game)

    return total_score


def pawn_structure(game):
    """
    Evaluate the pawn structure of the given chess position represented by `game`
    and return a numerical score representing the advantage of White over Black.
    The score is positive if White has a better pawn structure, negative if Black has
    a better pawn structure, and 0 if the pawn structure is roughly equal.

    The pawn structure is evaluated based on the following criteria:
    - Pawns on the same color as the player's bishop are penalized.
    - Doubled pawns are penalized.
    - Isolated pawns are penalized.
    - Backward pawns are penalized.
    - Control of the center by pawns is rewarded.
    - Passed pawns are rewarded.

    Args:
        game: A `chess.Board` object representing the current position.

    Returns:
        An integer representing the difference in pawn structure score between
        White and Black, with a positive value indicating an advantage for White
        and a negative value indicating an advantage for Black.
    """
    white_pawn_structure = 0
    black_pawn_structure = 0

    white_bishop_squares = set()
    black_bishop_squares = set()

    # Iterate over the board to find bishop squares
    for row in range(8):
        for col in range(8):
            square = game.board[row][col]
            if square != "--" and square[1] == "B":
                if square[0] == "w":
                    white_bishop_squares.add((row + col) % 2)
                else:
                    black_bishop_squares.add((row + col) % 2)

    # Iterate over the board
    for row in range(8):
        for col in range(8):
            square = game.board[row][col]

            # Check if the square contains a pawn
            if square != "--" and square[1] == "P":
                color = square[0]

                # Penalize for pawns on the same color as the player's bishop
                if (row + col) % 2 in white_bishop_squares and color == "w":
                    white_pawn_structure -= 1
                elif (row + col) % 2 in black_bishop_squares and color == "b":
                    black_pawn_structure -= 1

                # Check for doubled pawns
                if row > 0 and game.board[row - 1][col] == square:
                    if color == "w":
                        white_pawn_structure -= 1
                    else:
                        black_pawn_structure -= 1

                # Check for isolated pawns
                if col == 0 or col == 7 or (
                    (col > 0 and game.board[row][col - 1] != square)
                    and (col < 7 and game.board[row][col + 1] != square)
                ):
                    if color == "w":
                        white_pawn_structure -= 1
                    else:
                        black_pawn_structure -= 1

                # Check for backward pawns
                if (
                    row > 0
                    and col > 0
                    and col < 7
                    and game.board[row - 1][col - 1] != square
                    and game.board[row - 1][col + 1] != square
                ):
                    if color == "w":
                        white_pawn_structure -= 1
                    else:
                        black_pawn_structure -= 1

                # Reward center control
                if (col == 3 or col == 4) and (row >= 2 and row <= 5):
                    if color == "w":
                        white_pawn_structure += 1
                    else:
                        black_pawn_structure += 1

                # Check for passed pawns
                passed = True
                if color == "w":
                    for r in range(row - 1, -1, -1):
                        if game.board[r][col] != "--" and game.board[r][col][1] == "P":
                            passed = False
                            break
                else:
                    for r in range(row + 1, 8):
                        if game.board[r][col] != "--" and game.board[r][col][1] == "P":
                            passed = False
                            break

                if passed:
                    if color == "w":
                        white_pawn_structure += PASSED_PAWN_WEIGHT
                    else:
                        black_pawn_structure += PASSED_PAWN_WEIGHT

    return white_pawn_structure - black_pawn_structure


def evaluate_rooks(game):
    """
    Evaluate the rooks in the given chess position represented by `game`
    and return a numerical score representing the advantage of White over Black.
    The score is positive if White has a better rook placement, negative if Black has
    a better rook placement, and 0 if the rook placement is roughly equal.

    The rook placement is evaluated based on the following criteria:
    - Rooks on open files are rewarded.
    - Rooks on semi-open files are partially rewarded.
    - Rooks on the seventh rank are rewarded.
    - Rook mobility is rewarded.
    - Connected rooks are rewarded.

    Args:
        game: A `Game` object representing the current position.

    Returns:
        An integer representing the difference in rook placement score between
        White and Black, with a positive value indicating an advantage for White
        and a negative value indicating an advantage for Black.
    """
    white_rook_open_file = 0
    black_rook_open_file = 0
    white_rook_semi_open_file = 0
    black_rook_semi_open_file = 0
    white_rook_on_seventh = 0
    black_rook_on_seventh = 0
    white_rook_mobility = 0
    black_rook_mobility = 0
    white_connected_rooks = 0
    black_connected_rooks = 0

    for row in range(8):
        for col in range(8):
            square = game.board[row][col]
            if square != "--" and square[1] == "R":
                color = square[0]

                # Rook on open/semi-open file evaluation
                is_open_file = True
                is_semi_open_file = True  
                for r in range(8):
                    if r != row:
                        square = game.board[r][col]
                        if square != "--":
                            if square[1] == "P" and square[0] != color:
                                is_open_file = False
                            if square[1] == "P" and square[0] == color:
                                is_semi_open_file = False
                                break
                if is_open_file:
                    if color == "w":
                        white_rook_open_file += 1
                    else:
                        black_rook_open_file += 1
                elif is_semi_open_file:
                    if color == "w":
                        white_rook_semi_open_file += 1
                    else:
                        black_rook_semi_open_file += 1

                # Rook on the seventh rank evaluation
                if (color == "w" and row == 6) or (color == "b" and row == 1):
                    if color == "w":
                        white_rook_on_seventh += 1
                    else:
                        black_rook_on_seventh += 1

                # Rook mobility evaluation
                mobility = 0
                for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    r, c = row + dr, col + dc
                    while 0 <= r < 8 and 0 <= c < 8:
                        square = game.board[r][c]
                        if square == "--":
                            mobility += 1
                        elif square[0] != color:
                            mobility += 1
                            break
                        else:
                            break
                        r, c = r + dr, c + dc

                if color == "w":
                    white_rook_mobility += mobility
                else:
                    black_rook_mobility += mobility

    # Connected rooks evaluation
    for col1 in range(8):
        for col2 in range(col1 + 1, 8):
            if game.board[7][col1] == "wR" and game.board[7][col2] == "wR":
                white_connected_rooks += 1
                break

    for col1 in range(8):
        for col2 in range(col1 + 1, 8):
            if game.board[0][col1] == "bR" and game.board[0][col2] == "bR":
                black_connected_rooks += 1
                break

    return (ROOK_OPEN_FILE_WEIGHT * (white_rook_open_file - black_rook_open_file) +
            ROOK_SEMI_OPEN_FILE_WEIGHT * (white_rook_semi_open_file - black_rook_semi_open_file) +
            ROOK_ON_SEVENTH_WEIGHT * (white_rook_on_seventh - black_rook_on_seventh) +
            MOBILITY_WEIGHT * (white_rook_mobility - black_rook_mobility) +
            CONNECTED_ROOKS_WEIGHT * (white_connected_rooks - black_connected_rooks))


def piece_development(game):
    """
    Evaluate the piece development in the given chess position represented by `game`
    and return a numerical score representing the advantage of White over Black.
    The score is positive if White has better piece development, negative if Black has
    better piece development, and 0 if the piece development is roughly equal.

    The piece development is evaluated based on the following criteria:
    - Knights and bishops are rewarded for occupying optimal development squares.
    - Penalty for undeveloped pieces on their initial squares.

    Args:
        game: A `Game` object representing the current position.

    Returns:
        An integer representing the difference in piece development score between
        White and Black, with a positive value indicating an advantage for White
        and a negative value indicating an advantage for Black.
    """
    white_development = 0
    black_development = 0
    optimal_positions = {
        "wN": [(2, 2), (2, 5), (3, 3), (3, 4)],
        "wB": [(2, 2), (2, 5), (3, 3), (3, 4)],
        "bN": [(5, 2), (5, 5), (4, 3), (4, 4)],
        "bB": [(5, 2), (5, 5), (4, 3), (4, 4)],
    }

    for piece, start_positions in [('N', [(0, 1), (0, 6)]), ('B', [(0, 2), (0, 5)])]:
        for start_row, start_col in start_positions:
            square = game.board[start_row][start_col]
            if square != "--" and square[0] == 'w' and square[1] == piece:
                white_development -= 1
            for optimal_row, optimal_col in optimal_positions["w" + piece]:
                if game.board[optimal_row][optimal_col] == "w" + piece:
                    white_development += 1

    for piece, start_positions in [('N', [(7, 1), (7, 6)]), ('B', [(7, 2), (7, 5)])]:
        for start_row, start_col in start_positions:
            square = game.board[start_row][start_col]
            if square != "--" and square[0] == 'b' and square[1] == piece:
                black_development -= 1
            for optimal_row, optimal_col in optimal_positions["b" + piece]:
                if game.board[optimal_row][optimal_col] == "b" + piece:
                    black_development += 1

    return (white_development - black_development) * PIECE_DEVELOPMENT_WEIGHT


def king_safety(game):
    """
    Evaluate the king safety in the given chess position represented by `game`
    and return a numerical score representing the advantage of White over Black.
    The score is positive if White has a safer king, negative if Black has
    a safer king, and 0 if both kings are roughly equally safe.

    The king safety is evaluated based on the following criteria:
    - Penalty for exposed kings without adequate pawn and piece shields.
    - Bonus for king mobility.

    Args:
        game: A `Game` object representing the current position.

    Returns:
        An integer representing the difference in king safety score between
        White and Black, with a positive value indicating an advantage for White
        and a negative value indicating an advantage for Black.
    """

    def piece_shield(king_pos, color):
        """
        Calculates the shield score for the king of the specified color. The shield score is based on the pieces in front of the king
        that can protect it from enemy attacks. 

        Args:
        - king_pos: A tuple (row, col) representing the position of the king on the board.
        - color: A string "w" or "b" representing the color of the king.

        Returns:
        - The shield score for the king of the specified color, which is a weighted sum of the values of the pieces that form the shield.
        """        
        shield_score = 0
        shield_pieces = ["P", "N", "B", "R", "Q"]
        row_direction = -1 if color == "w" else 1
        shield_row = king_pos[0] + row_direction
        pinned_positions = [(pin[0], pin[1]) for pin in game.pins]

        if 0 <= shield_row < 8:
            for col_offset in range(-1, 2):
                col = king_pos[1] + col_offset
                if 0 <= col < 8:
                    square = game.board[shield_row][col]
                    if square != "--" and square[0] == color and square[1] in shield_pieces:
                        piece_pos = (shield_row, col)
                        if piece_pos not in pinned_positions:
                            shield_score += PIECE_SCORE[square[1]] 

        return shield_score * PIECE_SHIELD_WEIGHT

    def king_mobility(king_pos):
        """
        Calculates the mobility score for the king. The mobility score is based on the number of squares the king can move to without
        being under attack.

        Args:
        - king_pos: A tuple (row, col) representing the position of the king on the board.

        Returns:
        - The mobility score for the king, which is a weighted sum of the number of squares the king can move to without being under attack.
        """
        mobility_score = 0
        king_moves = set()
        game.get_king_moves(king_pos[0], king_pos[1], king_moves)

        for move in king_moves:
            if not game.cell_under_attack(move.end_row, move.end_col):
                mobility_score += 1

        return mobility_score * KING_MOBILITY_WEIGHT

    white_king_safety = 0
    black_king_safety = 0
    white_king_safety += piece_shield(game.white_king_pos, "w")
    black_king_safety += piece_shield(game.black_king_pos, "b")
    white_king_safety += king_mobility(game.white_king_pos)
    black_king_safety += king_mobility(game.black_king_pos)

    return KING_SAFETY_WEIGHT * (white_king_safety - black_king_safety)


def center_control(game):
    '''
    Calculate the center control score for a chess game.

    The function iterates over the board and checks for all pieces and their valid moves. 
    It counts the number of valid moves that attack center squares, and sums up the total center control for both white and black pieces.

    Args:
        game: A `Game` object representing the current position.

    Returns:
        float: The difference between white center control score and black center control score, multiplied by `CENTER_CONTROL_WEIGHT`.
    '''
    center_squares = {(2, 2), (2, 3), (2, 4), (2, 5),
                      (3, 2), (3, 3), (3, 4), (3, 5),
                      (4, 2), (4, 3), (4, 4), (4, 5),
                      (5, 2), (5, 3), (5, 4), (5, 5)}
    white_center_control = 0
    black_center_control = 0

    # Function to count center attacks
    def count_center_attacks(valid_move_set, attacking_piece_score):
        count = 0
        for move in valid_move_set:
            if (move.end_row, move.end_col) in center_squares:
                count += attacking_piece_score
        return count

    # Iterate over the board
    for row in range(8):
        for col in range(8):
            square = game.board[row][col]
            if square != '--':
                piece_color = square[0]
                piece_type = square[1]
                valid_move_set = set()

                if piece_type == 'P':
                    game.get_pawn_moves(row, col, valid_move_set)
                elif piece_type == 'R':
                    game.get_rook_moves(row, col, valid_move_set)
                elif piece_type == 'N':
                    game.get_knight_moves(row, col, valid_move_set)
                elif piece_type == 'B':
                    game.get_bishop_moves(row, col, valid_move_set)
                elif piece_type == 'Q':
                    game.get_queen_moves(row, col, valid_move_set)
                # Exclude king moves
                elif piece_type == 'K':
                    continue

                attacking_piece_score = PIECE_SCORE[piece_type]
                if piece_color == 'w':
                    white_center_control += count_center_attacks(valid_move_set, attacking_piece_score)
                else:
                    black_center_control += count_center_attacks(valid_move_set, attacking_piece_score)

    return (white_center_control - black_center_control) * CENTER_CONTROL_WEIGHT

def mobility(game):
    '''
    The function takes a Game object representing the current state of the game as an argument 
    and calculates the normalized mobility for the current player by dividing the total number of 
    valid moves by the approximate total number of legal moves in a chess game. The result is multiplied 
    by MOBILITY_WEIGHT and returned as a positive value for the player with the next move and a negative 
    value for the opponent.

    Args:
        game: A `Game` object representing the current position.

    Returns:
        float: The mobility score, as a positive value for the player with the next move and a negative value for the opponent.
    '''
    valid_moves = game.get_valid_moves()
    normalized_mobility = len(valid_moves) / 4672  # 4672 is the approximate total number of legal moves in a chess game
    return normalized_mobility * MOBILITY_WEIGHT if game.white_to_move else -normalized_mobility * MOBILITY_WEIGHT


#########################
### THE MIN MAX ALGORITHM WITH MVV-LVA MOVE ORDERING AND MOVE REDUCTION
######################### 
def find_good_move(game, valid_move_set): 

    def mvv_lva_score(move):
        start_piece = game.board[move.start_row][move.start_col]
        end_piece = game.board[move.end_row][move.end_col]
        
        attacker_value = PIECE_SCORE[start_piece[1]] if start_piece != "--" else 0
        victim_value = PIECE_SCORE[end_piece[1]] if end_piece != "--" else 0
        
        score = 15 * (victim_value - attacker_value)
        if (move.end_row in (3, 4)) and (move.end_col in (3, 4)):
            score += 7
        return score if game.white_to_move else -score

    def reduction_factor(depth, move_number):
        if depth < 3:
            return 0
        return max(1, int(math.log(depth + 1) * math.log(move_number + 1)))

    def find_move_minmax(valid_move_set, depth, alpha, beta, maximizing_player, move_number):
        zobrist_hash = compute_zobrist_hash(game)
        cached_entry = TRANSPOSITION_TABLE.lookup(zobrist_hash)

        if cached_entry and cached_entry["depth"] >= depth:
            return cached_entry["score"], cached_entry["move"]

        if depth == 0 or game.check_mate or game.stale_mate:
            return score_board(game), None

        best_score = -CHECKMATE if maximizing_player else CHECKMATE
        best_move = None

        valid_move_list = list(valid_move_set)
        valid_move_list.sort(key=mvv_lva_score, reverse=maximizing_player)

        lmr_threshold = 4
        move_number = 0

        for move in valid_move_list:
            game.make_move(move)
            if move_number >= lmr_threshold:
                r = reduction_factor(depth, move_number)
                reduced_depth = max(depth - 1 - r, 0)
                curr_score, _ = find_move_minmax(game.get_valid_moves(), reduced_depth, alpha, beta, not maximizing_player, move_number)
            else:
                curr_score, _ = find_move_minmax(game.get_valid_moves(), depth - 1, alpha, beta, not maximizing_player, move_number)
            game.undo_move()

            if maximizing_player:
                if curr_score > best_score:
                    best_score = curr_score
                    best_move = move
                alpha = max(alpha, best_score)
            else:
                if curr_score < best_score:
                    best_score = curr_score
                    best_move = move
                beta = min(beta, best_score)

            if beta <= alpha:
                break

            move_number += 1

        TRANSPOSITION_TABLE.store(zobrist_hash, {"depth": depth, "score": best_score, "move": best_move})
        return best_score, best_move

    best_score, best_move = find_move_minmax(valid_move_set, DEPTH, -CHECKMATE, CHECKMATE, game.white_to_move, 0)
    return (best_score, best_move)

#########################
### RUNNING MIN MAX CONCURRENT
######################### 
def run_concurrent(game, valid_moves, maximizing_player):
    num_processes = multiprocessing.cpu_count() - 1  # Leave one core for the main process and other system tasks
    num_processes = max(1, num_processes)  # Ensure at least one process is used

    move_subsets = [(list(valid_moves))[i::num_processes] for i in range(num_processes)]
    game_copies = [copy.deepcopy(game) for _ in range(num_processes)]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(find_good_move, game_copies[i], move_subset) for i, move_subset in enumerate(move_subsets)]

    # accumulate the results
    results = [future.result() for future in futures]

    # return the move with the highest score
    if maximizing_player:
        return max(results, key=lambda x: x[0])
    else:
        return min(results, key=lambda x: x[0])

#########################
### MAIN FUNCTION
######################### 
def run_engine(game, valid_move_set):
    return run_concurrent(game, valid_move_set, game.white_to_move)[1]
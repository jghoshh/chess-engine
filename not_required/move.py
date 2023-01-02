### THE MOVE CLASS

RANKS_TO_ROWS = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
ROW_TO_RANKS = {value: key for key, value in RANKS_TO_ROWS.items()}
FILES_TO_COLS = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
COLS_TO_FILES = {value: key for key, value in FILES_TO_COLS.items()}


### Validates and moves a piece and returns a tuple containing the moved piece and the captured piece. 
def make_move(start_row, start_col, end_row, end_col, board): 

    piece_moved = board[start_row][start_col]

    if (piece_moved) == "--": 
        piece_moved = None

    piece_captured = board[end_row][end_col]
    if (piece_captured) == "--": 
        piece_captured = None

    if piece_moved != None: 
        board[start_row][start_col] = "--"
        board[end_row][end_col] = piece_moved
    
    return (piece_moved, piece_captured)


### Convert a move to chess notation
def convert_to_c(move): 

    if (move[0] == None and move[1] == None): 
        return "irrelevant move"

    if (move[0] == None): 
        return "invalid move"

    return COLS_TO_FILES[move[2]] + ROW_TO_RANKS[move[3]] + COLS_TO_FILES[move[4]] + ROW_TO_RANKS[move[5]]


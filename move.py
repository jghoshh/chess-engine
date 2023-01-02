ROW_TO_RANKS = {7:"1", 6:"2", 5:"3", 4:"4", 3:"4", 2:"6", 1:"7", 0:"8"}
COLS_TO_FILES = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}

class Move(): 

    def __init__(self, start, end, board): 
        self.start_row = start[0]
        self.start_col = start[1]
        self.end_row = end[0]
        self.end_col = end[1]
        self.piece_captured = board[self.end_row][self.end_col]
        self.piece_moved = board[self.start_row][self.start_col]

    def __hash__(self):
        return hash(self.key())
    
    def key(self): 
        return (self.start_row, self.start_col, self.end_row, self.end_col, self.piece_captured, self.piece_moved)

    def __eq__(self, other):
        if isinstance(other, Move):
            # Instead of doing such a long and statement, we could assign an id to each move. 
            return self.start_row == other.start_row and self.start_col == other.start_col and self.end_row == other.end_row and self.end_col == other.end_col and self.piece_captured == other.piece_captured and self.piece_moved == other.piece_moved 
        return False

    def __repr__(self): 
        return COLS_TO_FILES[self.start_row] + ROW_TO_RANKS[self.start_col] + COLS_TO_FILES[self.end_row] + ROW_TO_RANKS[self.end_col]

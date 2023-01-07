### CLASS MODULE (MOVE) THAT IS THE FUNDAMETAL BUILDING BLOCK OF OUR ENGINE. STORES THE DETAILS ABOUT A MOVE THAT CAN AND/OR HAS OCCURED IN A GAME.
ROW_TO_RANKS = {7:"1", 6:"2", 5:"3", 4:"4", 3:"4", 2:"6", 1:"7", 0:"8"}
COLS_TO_FILES = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}

class Move(): 

    def __init__(self, start, end, board, castling_move=False): 
        self.start_row = start[0]
        self.start_col = start[1]
        self.end_row = end[0]
        self.end_col = end[1]
        self.piece_captured = board[self.end_row][self.end_col]
        self.piece_moved = board[self.start_row][self.start_col]
        self.castling_move = castling_move
        self.id = self.__hash__()

    # need to define a hash function because we are using a set to store valid moves.
    def __hash__(self):
        return hash(self.key())
    
    def key(self): 
        return (self.start_row, self.start_col, self.end_row, self.end_col, self.piece_captured, self.piece_moved, self.castling_move)

    def __eq__(self, other):
        # need is instance here to inspect appropriate attributes.
        if isinstance(other, Move):
            return (self.start_row, self.start_col, self.end_row, self.end_col, self.piece_captured, self.piece_moved, self.castling_move) == (other.start_row, other.start_col, other.end_row, other.end_col, other.piece_captured, other.piece_moved, other.castling_move)
        return False

    def __repr__(self): 
        return  COLS_TO_FILES[self.start_col] + ROW_TO_RANKS[self.start_row] + COLS_TO_FILES[self.end_col] + ROW_TO_RANKS[self.end_row]

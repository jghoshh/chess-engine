### MODULE RESPONSIBLE FOR HANDLING THE BACKEND OF THE CHESS GAME.
import numpy as np

RANKS_TO_ROWS = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
ROW_TO_RANKS = {value: key for key, value in RANKS_TO_ROWS.items()}
FILES_TO_COLS = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
COLS_TO_FILES = {value: key for key, value in FILES_TO_COLS.items()}


### This class defines and records the state of the chess game being played.
class Game():

    def __init__(self): 

        #The chess board. 
        self.board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"], 
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"], 
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"], 
        ]

        # We will maintain an instance variable that checks if it is white's turn to move or not.
        # Note, we will perceive the game from the perspective of white and only white.
        self.white_to_move = True

        # We will also maintain a move log, registering all the moves that occured in the game.
        self.move_log = []

    # Function to validate the move and record it in the move_log.
    def make_move(self, move): 
        
        #deciphering the move into starting row, starting column, ending row, and ending column.
        start_row = move[0][0]
        start_col = move[0][1]
        end_row = move[1][0]
        end_col = move[1][1]

        piece_moved = self.board[start_row][start_col]
        
        if (piece_moved) == "--": 
            piece_moved = None

        piece_captured = self.board[end_row][end_col]
        if (piece_captured) == "--": 
            piece_captured = None

        if piece_moved != None: 
            self.board[start_row][start_col] = "--"
            self.board[end_row][end_col] = piece_moved

        if not ((piece_moved == None and piece_captured == None) or (piece_moved == None and piece_captured != None)): # Only append to move log if the move is valid.
            self.move_log.append((piece_moved, piece_captured, move[0][0], move[0][1], move[1][0], move[1][1])) # PIECE MOVED, PIECE CAPTURED, STARTING ROW, STARTING COL, ENDING ROW, ENDING COL
            self.white_to_move = not self.white_to_move # switch player turns.

    # Function to reverse/undo the most recent move. 
    def undo_move(self): 
        if self.move_log: 
            res = self.move_log.pop()
            start_row = res[4]
            start_col = res[5]
            end_row = res[2]
            end_col = res[3]
            piece_moved = self.board[start_row][start_col]
            self.board[start_row][start_col] = "--"
            self.board[end_row][end_col] = piece_moved
            self.white_to_move = not self.white_to_move

    ### Most complicated part probably. 
    ### The following functions aid in validating moves.
    ### The main concept behind generating valid moves is that you have to generate the other player's moves to ensure that your move 
    ### doesn't result in the other player putting you in check. 

    #### Pseudocode: 
    #### Get all possible moves
    #### For each possible move, do the following to check if it is a valid move: 
    #### Make the move
    #### Generate all the possible moves for the other player.
    #### See if any of the moves of the other player attacks your king.
    #### If there is no attack, then the move is valid.
    #### Else, undo the move. The move is not valid. 

    # Function to get all possible moves, without considering any checks. 
    def get_all_moves(self):
        print("being run again")

        all_moves = set()

        for i in range(len(self.board)): 
            for j in range(len(self.board[0])): 
                
                piece = self.board[i][j]
                
                if piece != '--' and ((piece[0] == 'w' and self.white_to_move) or (piece[0] == 'b' and not self.white_to_move)): 
                    
                    piece_type = piece[1]
    
                    if piece_type == 'P': 
                        self.get_pawn_moves(i, j, all_moves)

        return all_moves
                    
    # Function to get all possible moves, with considering checks. These are valid moves. 
    def get_valid_moves(self): 
        return self.get_all_moves()

    
    def get_pawn_moves(self, row, col, valid_move_set): 
        #if it is white's turn to move, then we will compute the valid moves of the white pawns.
        if self.white_to_move: 
            
            if self.board[row-1][col] == '--': # Moving one step in general.
                valid_move_set.add(((row, col), (row - 1, col)))
            
            if row == 6 and self.board[row-2][col] == '--': # Moving two steps from the start.
                valid_move_set.add(((row, col), (row - 2, col)))

    
    def convert_to_c(self, move): 

        if (move[0] == None and move[1] == None): 
            return "irrelevant move"

        if (move[0] == None): 
            return "invalid move"

        return COLS_TO_FILES[move[2]] + ROW_TO_RANKS[move[3]] + COLS_TO_FILES[move[4]] + ROW_TO_RANKS[move[5]]







        







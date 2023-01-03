### MODULE RESPONSIBLE FOR HANDLING THE BACKEND OF THE CHESS GAME.
from move import Move
from collections import deque
import numpy as np

### This class defines and records the state of the chess game being played.
class Game():

    def __init__(self): 

        #The chess board. 
        self.board = np.array([ 
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"], 
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"], 
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"], 
        ])

        # We will maintain an instance variable that checks if it is white's turn to move or not.
        # Note, we will perceive the game from the perspective of white and only white.
        self.white_to_move = True

        # We will also maintain a move log, registering all the moves that occured in the game.
        self.move_log = deque()

        # Dictionary for function calls for more elegant code. 
        self.move_functions = {'P': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves, 
        'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}

    # Function to make the move. 
    def make_move(self, move): 
        if move.piece_moved != None: 
            self.board[move.end_row][move.end_col] = move.piece_moved
            self.board[move.start_row][move.start_col] = "--"
            self.move_log.append(move)
            self.white_to_move = not self.white_to_move

    # Function to reverse/undo the most recent move. 
    def undo_move(self): 
        if self.move_log: 
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
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
        
        all_moves = set()

        for i in range(len(self.board)): 
            for j in range(len(self.board[0])): 
                
                piece = self.board[i][j]
                
                if piece != '--' and ((piece[0] == 'w' and self.white_to_move) or (piece[0] == 'b' and not self.white_to_move)): 
                    self.move_functions[piece[1]](i, j, all_moves)

        print(all_moves)
        return all_moves
                    
    # Function to get all possible moves, with considering checks. These are valid moves. 
    def get_valid_moves(self): 
        return self.get_all_moves()
    
    def get_pawn_moves(self, row, col, valid_move_set): 
        # if it is white's turn to move, then we will compute the valid moves of the white pawns.
        if self.white_to_move: 
            
            # Navigating to empty squares. No captures are considered here.
            if self.board[row-1][col] == '--': # Moving one step in general.
                valid_move_set.add(Move((row, col), (row-1, col), self.board))

                if row == 6 and self.board[row-2][col] == '--': # Moving two steps from the start.
                    valid_move_set.add(Move((row, col), (row-2, col), self.board))

            # Now, we consider captures. 
            # Consider captures to the left: 
            if row > 0 and col - 1 >= 0: 
                # if there is an enemy piece to capture to the left.
                if self.board[row-1][col-1][0] == 'b': 
                    valid_move_set.add(Move((row, col), (row-1, col-1), self.board))

            # Consider captures to the right: 
            if row > 0 and col + 1 <= len(self.board) - 1:  
                # if there is an enemy piece to capture to the right.
                if self.board[row-1][col+1][0] == 'b': 
                    valid_move_set.add(Move((row, col), (row-1, col+1), self.board))

        # if it not white's turn, we consider black pawn moves. 
        else: 
            # Navigating to empty squares. No captures are considered here.
            if self.board[row+1][col] == '--': # Moving one step in general.
                valid_move_set.add(Move((row, col), (row+1, col), self.board))

                if row == 1 and self.board[row+2][col] == '--': # Moving two steps from the start.
                    valid_move_set.add(Move((row, col), (row+2, col), self.board))

            # Now, we consider captures. 
            # Consider captures to the left: 
            if row < len(self.board) - 1 and col - 1 >= 0: 
                # if there is an enemy piece to capture to the left.
                if self.board[row+1][col-1][0] == 'w': 
                    valid_move_set.add(Move((row, col), (row+1, col-1), self.board))

            # Consider captures to the right: 
            if row < len(self.board) - 1 and col + 1 <= len(self.board) - 1:  
                # if there is an enemy piece to capture to the right.
                if self.board[row+1][col+1][0] == 'w': 
                    valid_move_set.add(Move((row, col), (row+1, col+1), self.board))


    def get_rook_moves(self, row, col, valid_move_set): 

        # Get the directions that the rook can possibly move in. 
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        for d in range(len(directions)): 
            for i in range(1, len(self.board)): 
                ending_row = r + 

    def get_knight_moves(self, row, col, valid_move_set):
        print("get_knight_moves")
        pass

    def get_bishop_moves(self, row, col, valid_move_set): 
        print("get_bishop_moves")
        pass

    def get_king_moves(self, row, col, valid_move_set): 
        print("get_king_moves")
        pass

    def get_queen_moves(self, row, col, valid_move_set): 
        print("get_queen_moves")
        pass
    







        







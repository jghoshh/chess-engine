### MODULE RESPONSIBLE FOR HANDLING THE BACKEND OF THE CHESS GAME.
import numpy as np
from move import move

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
    def validate_and_move(self, start, end): 
        res = move(start[0], start[1], end[0], end[1], self.board)
        if not ((res[0] == None and res[1] == None) or (res[0] == None and res[1] != None)): # Only append to move log if the move is valid.
            self.move_log.append((res[0], res[1], start[0], start[1], end[0], end[1])) # PIECE MOVED, PIECE CAPTURED, STARTING ROW, STARTING COL, ENDING ROW, ENDING COL
            self.white_to_move = not self.white_to_move # switch player turns.

    # Function to reverse/undo the most recent move. 
    def undo_move(self): 
        if self.move_log: 
            res = self.move_log.pop()
            move(res[4], res[5], res[2], res[3], self.board)
            self.white_to_move = not self.white_to_move

    ### Most complicated part probably. 







        







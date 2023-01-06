### MODULE RESPONSIBLE FOR HANDLING THE BACKEND OF THE CHESS GAME.
from move import Move
from castle_check import CastleCheck
from copy import deepcopy
from collections import deque

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
        self.move_log = deque()

        # Dictionary for function calls for more elegant code. 
        self.move_functions = {'P': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves, 
        'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}

        # To deal with checks, checkmate, stalemate, or castling will need to store the
        # current positions of the two kings on the board. In our get_valid_moves function, 
        # we will utilize these two positions to generate valid moves.
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)

        # We need a variable to determine if the player is currently in check or not. 
        self.in_check = False

        # We need a variable to determine if a checkmate has occured or not. 
        self.check_mate = False

        # We need a variable to determine if a stalemate has occured or not.
        self.stale_mate = False

        # Suppose there is a pin, we need to store the pieces that are pinned, because we
        # cannot move them. 
        self.pins = []

        # Store the positions where the opponent has a piece that is checking the player's king.
        self.checks = []

        # We need a variable to determine if any castling rule has been broken.
        self.current_castling_check = CastleCheck(True, True, True, True)

        # We need a variable to keep track of the moves that affect castling rules.
        self.castling_check_log = deque()
        self.castling_check_log.append(deepcopy(self.current_castling_check))

    # Function to make the move. 
    def make_move(self, move): 

        if move.piece_moved != None:
                print(move.piece_moved)
                self.board[move.end_row][move.end_col] = move.piece_moved
                self.board[move.start_row][move.start_col] = "--"
                self.move_log.append(move)
                self.white_to_move = not self.white_to_move

                if (move.piece_moved == 'wK'): self.white_king_pos = (move.end_row, move.end_col)
                elif (move.piece_moved == 'bK'): self.black_king_pos = (move.end_row, move.end_col)

                if move.castling_move: 
                    # kingside castle.
                    if (move.end_col - move.start_col) == 2:
                        self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]
                        self.board[move.end_row][move.end_col + 1] = '--'
                    else: 
                        self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2]
                        self.board[move.end_row][move.end_col - 2] = '--'

                self.update_castle_check(move)
                self.castling_check_log.append(CastleCheck(self.current_castling_check.wks, self.current_castling_check.bks, self.current_castling_check.wqs, self.current_castling_check.bqs))

    # Function to reverse/undo the most recent move. 
    def undo_move(self): 
        if self.move_log: 
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

            # update king positions.
            if (move.piece_moved == 'wK'):
                self.white_king_pos = (move.start_row, move.start_col)
            elif (move.piece_moved == 'bK'): 
                self.black_king_pos = (move.start_row, move.start_col)
            
            #undo castle move.
            if move.castling_move: 
                #kingside undo.
                if (move.end_col - move.start_col) == 2: 
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = '--'
                #queenside undo.
                else: 
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = '--'

            self.castling_check_log.pop()
            most_recent_castle_state = self.castling_check_log[-1]
            self.current_castling_check.wks, self.current_castling_check.wqs, self.current_castling_check.bks, self.current_castling_check.bqs = most_recent_castle_state.wks, most_recent_castle_state.wqs, most_recent_castle_state.bks, most_recent_castle_state.bqs

    # Function to get all possible moves, without considering any checks. 
    def get_all_moves(self):

        if self.white_to_move: king_row, king_col = self.white_king_pos
        else: king_row, king_col = self.black_king_pos

        all_moves = set()

        for i in range(len(self.board)): 
            for j in range(len(self.board[i])): 
                
                piece = self.board[i][j]
                
                if piece != '--' and ((piece[0] == 'w' and self.white_to_move) or (piece[0] == 'b' and not self.white_to_move)): 
                    self.move_functions[piece[1]](i, j, all_moves)
        
        return self.get_castle_moves(king_row, king_col, all_moves)
                    
    # Function to get all possible moves, with considering checks. These are valid moves. 
    def get_valid_moves(self): 

        valid_moves = set()
        valid_cells = set()
        self.find_pins_and_checks()

        if self.white_to_move: king_row, king_col = self.white_king_pos
        else: king_row, king_col = self.black_king_pos
        
        # if the king is in check,
        if self.in_check: 
            # if the king is checked in only one way, either move the king or block the check.
            if len(self.checks) == 1: 
                valid_moves = self.get_all_moves()

                # we analyze the check by getting the attacking piece, the row, and the col.
                check_row = self.checks[0][0]
                check_col = self.checks[0][1]
                attacker = self.board[check_row][check_col]

                # if the attacker is a knight, the only ways to block the check are to either move the king or capture the knight.
                # we define a valid cells set to contain all the cells that pieces other than the king can move to when a check is caused.
                # we populate valid cells starting with the case of a knight checking.
                if attacker[1] == 'N': 
                    valid_cells = {(check_row, check_col)}
                else: 
                    # if the attacker is not a knight, we can possibly block the check with another piece in the direction of the attack.
                    # in other words, we can intentionally pin a piece in the direction of the check.
                    for i in range(1, 8): 
                        valid_cell = (king_row + (self.checks[0][2] * i), king_col + (self.checks[0][3] * i))
                        valid_cells.add(valid_cell)

                        # our limitations of blocking the check go from pinning a piece intentionally to capturing the attacker.
                        # after that we don't inspect any further.
                        if valid_cell[0] == check_row and valid_cell[1] == check_col: 
                            break
                    
                    # filter all the valid moves such that only the moves that end up in the valid cells remain.
                    valid_moves = set(filter(lambda move: move.piece_moved[1] == 'K' or ((move.end_row, move.end_col) in valid_cells), valid_moves))
                    
            # double check
            else: 
                self.get_king_moves(king_row, king_col, valid_moves)

            if len(valid_moves) == 0:
                if self.in_check: 
                    self.check_mate = True
                    print("checkmate")
                else: 
                    self.state_mate = True
            else: 
                # need this in case we undo we need to reset any checkmates or statemates.
                self.check_mate = False
                self.state_mate = False

        else: 
            #if the king is not in check, then all moves should be valid, minus the ones that directly lead to the king being in check, i.e. pins.
            return self.get_all_moves()

        return valid_moves

    
    def update_castle_check(self, move): 
        if move.piece_moved == 'wK': 
            self.current_castling_check.wks = False
            self.current_castling_check.wqs = False
            
        elif move.piece_moved == 'bK': 
            self.current_castling_check.bks = False
            self.current_castling_check.bqs = False

        elif move.piece_moved == 'wR': 
            if move.start_row == 7 and move.start_col == 0: 
                self.current_castling_check.wqs = False
            elif move.start_row == 7 and move.start_col == 7: 
                self.current_castling_check.wks = False

        elif move.piece_moved == 'bR': 
            if move.start_row == 0 and move.start_col == 0: 
                self.current_castling_check.bqs = False
            elif move.start_row == 0 and move.start_col == 7: 
                self.current_castling_check.bks = False

        if move.piece_captured == 'wR':
            if move.end_row == 7 and move.end_col == 0: 
                self.current_castling_check.wqs = False
            elif move.end_row == 7 and move.end_col == 7:
                self.current_castling_check.wks = False

        elif move.piece_captured == 'bR':
            if move.end_row == 0 and move.end_col == 0: 
                self.current_castling_check.bqs = False
            elif move.end_row == 0 and move.end_col == 7:
                self.current_castling_check.bks = False

        
    def find_pins_and_checks(self): 

        # first, determine whose turn it is, what the player colour is, what the opponent colour is, 
        # and where the player's king is located.
        enemy_colour = 'w'
        piece_colour = 'b'
        king_row, king_col = self.black_king_pos
        if self.white_to_move: 
            enemy_colour = 'b' 
            piece_colour = 'w'
            king_row, king_col = self.white_king_pos
        
        pins = []
        checks = []
        in_check = False
        # every possible direction from the king's location that can prodcue a check. 
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        # iterate over every possible direction that can produce a check.
        for dr in range(len(directions)): 

            # look out for any possible pins.
            pin = ()
            
            # for each direction, check every possible cell in that direction.
            for i in range(1, len(self.board)): 
                
                end_row = king_row + (directions[dr][0] * i)
                end_col = king_col + (directions[dr][1] * i)
    
                # if the cell coordinates are within the bounds of the board, proceed to process it further.
                if (end_row < len(self.board) and end_row >= 0 and end_col < len(self.board) and end_col >= 0): 

                    end_pos = self.board[end_row][end_col]
                    
                    # if the cell contains a piece of the same colour as the player, then check for in a pin was registered previously
                    # in this direction. If not, then this piece is a possible pin.
                    if end_pos[0] == piece_colour and not pin: 
                        pin = (end_row, end_col, directions[dr][0], directions[dr][1])
                    
                    # if a pin was already registered in this direction, no need to check any more pieces in this direction. 
                    # regardless of if there was an attacker in this direction, the intial pin in this direction will prevent
                    # any checks.
                    elif end_pos[0] == piece_colour and pin: 
                        break

                    # if an enemy piece is encountered in this direction, we must check if it possible for this piece to attack us.
                    # we will cehck this by matching the piece type against the direction we are currently inspecting. 

                    elif end_pos[0] == enemy_colour: 
                        piece_type = end_pos[1]

                        # check if there is a rook attacking from any orthagonal direction from the king.
                        rook_check = dr >= 0 and dr <= 3 and piece_type == 'R'

                        # check if there is a bishop attacking from any diagonal direction from the king.
                        bishop_check = dr >= 4 and dr <= 7 and piece_type == 'B'

                        # check if there is a pawn attacking. There are two conditions for this.
                        # if the player colour is white, then the pawn must be a black pawn, and 
                        # must be attacking downwards and in a diagonal direction of one cell.
                        # however, if the player colour is black, then the pawn must be a white pawn
                        # and must be attacking upwards and in a diagonal direction of one cell.
                        pawn_check = i == 1 and piece_type == 'P' and ((enemy_colour == 'b' and (dr == 4 or dr == 5)) or (enemy_colour == 'w' and (dr == 6 or dr == 7)))

                        # although kings can't check other kings, we need to ensure that
                        # there are no kings one square away, because it is an invalid
                        # position.
                        king_avoidance = i == 1 and piece_type == 'K'

                        if rook_check or bishop_check or pawn_check or king_avoidance or piece_type == 'Q': 

                            # if there is an attacker in a direction that they can attack in, then there is a possible check.
                            # if there is no ally piece in this same direction, then there is no pin, and thus a check is confirmed.
                            if not pin: 
                                in_check = True
                                # append this check to the list of checks.
                                checks.append((end_row, end_col, directions[dr][0], directions[dr][1]))
                                # don't check in this direction further, as only one piece can check in any given direction.
                                break
                            
                            # if there is a piece in the way and there is a possible check in the same direction, a pin is confirmed.
                            else: 
                                pins.append(pin)
                                # don't check in this direction further, as no other checks or pins are further possible.
                                break
                        
                        else: 
                            # if the first enemy piece in this direction, is not a valid attacker, i.e. they cannot apply a check from where they are, then don't check this direction further.
                            break
        
        
        # for knights, it is a bit different to check for checks. A pin is not possible with a knight.
        directions = [(-1, -2), (1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1)]

        for dr in directions: 
            end_row = king_row + dr[0]
            end_col = king_col + dr[1]

            # if the cell coordinates are within the bounds of the board, proceed to process it further.
            if (end_row < len(self.board) and end_row >= 0 and end_col < len(self.board) and end_col >= 0): 

                end_pos = self.board[end_row][end_col]
                
                if (end_pos[1] == 'N' and end_pos[0] == enemy_colour): 
                    in_check = True
                    checks.append((end_row, end_col, dr[0], dr[1]))
        
        self.in_check = in_check
        self.pins = pins
        self.checks = checks

    def get_pawn_moves(self, row, col, valid_move_set): 

        # logic to ensure that pinned pawns cannot move.
        piece_pinned = False
        direction = ()

        # go through the generated pins and check if the current piece is pinned.
        pin = None
        for pin in self.pins: 
            if pin[0] == row and pin[1] == col: 
                piece_pinned = True
                direction = (pin[2], pin[3])
                break

        if pin and piece_pinned: self.pins.remove(pin)

        # if it is white's turn to move, then we will compute the valid moves of the white pawns.
        if self.white_to_move: 
            
            # Navigating to empty squares. No captures are considered here.
            if self.board[row-1][col] == '--': # Moving one step in general.

                # if the piece is not pinned, or if the pin is in the natural direction that the piece moves in,
                # then moving the piece is OK.
                if not piece_pinned or direction == (-1, 0):
                    valid_move_set.add(Move((row, col), (row-1, col), self.board))

                    if row == 6 and self.board[row-2][col] == '--': # Moving two steps from the start.
                        valid_move_set.add(Move((row, col), (row-2, col), self.board))

            # Now, we consider captures. 
            # Consider captures to the left: 
            if row > 0 and col - 1 >= 0: 
                # if there is an enemy piece to capture to the left.
                if self.board[row-1][col-1][0] == 'b': 
                    if not piece_pinned or direction == (-1, -1): 
                        valid_move_set.add(Move((row, col), (row-1, col-1), self.board))

            # Consider captures to the right: 
            if row > 0 and col + 1 <= len(self.board) - 1:  
                # if there is an enemy piece to capture to the right.
                if self.board[row-1][col+1][0] == 'b': 
                    if not piece_pinned or direction == (-1, 1): 
                        valid_move_set.add(Move((row, col), (row-1, col+1), self.board))

        # if it not white's turn, we consider black pawn moves. 
        else: 
            # Navigating to empty squares. No captures are considered here.
            if self.board[row+1][col] == '--': # Moving one step in general.
                if not piece_pinned or direction == (1, 0):
                    valid_move_set.add(Move((row, col), (row+1, col), self.board))

                    if row == 1 and self.board[row+2][col] == '--': # Moving two steps from the start.
                        valid_move_set.add(Move((row, col), (row+2, col), self.board))

            # Now, we consider captures. 
            # Consider captures to the left: 
            if row < len(self.board) - 1 and col - 1 >= 0: 
                # if there is an enemy piece to capture to the left.
                if self.board[row+1][col-1][0] == 'w':
                    if not piece_pinned or direction == (1, -1): 
                        valid_move_set.add(Move((row, col), (row+1, col-1), self.board))

            # Consider captures to the right: 
            if row < len(self.board) - 1 and col + 1 <= len(self.board) - 1:  
                # if there is an enemy piece to capture to the right.
                if self.board[row+1][col+1][0] == 'w':
                    if not piece_pinned or direction == (1, 1): 
                        valid_move_set.add(Move((row, col), (row+1, col+1), self.board))


    def get_rook_moves(self, row, col, valid_move_set): 
        self.get_bishop_or_rook_moves(row, col, valid_move_set)


    def get_knight_moves(self, row, col, valid_move_set):
        self.get_king_or_knight_moves(row, col, valid_move_set, king=False)


    def get_bishop_moves(self, row, col, valid_move_set): 
        self.get_bishop_or_rook_moves(row, col, valid_move_set, rook=False)

    def get_king_moves(self, row, col, valid_move_set): 
        self.get_king_or_knight_moves(row, col, valid_move_set, king=True)


    def get_queen_moves(self, row, col, valid_move_set): 
        # if a queen is pinned, we need to create two pin lists and send them to the bishop or rook move generating function. 
        # otherwise, the queen pin will be removed in the rook function and diagonal queen moves will be valid, as all bishop moves will be perceived to be valid.
        self.get_bishop_or_rook_moves(row, col, valid_move_set, rook=True)
        self.get_bishop_or_rook_moves(row, col, valid_move_set, rook=False)


    # Since both bishops and rooks follow the same algorithm to compute valid moves, for the sake of design, we will design a generic function
    # that is controlled by a flag variable indicating whether is the bishop or the rook's moves which need to be computed. 
    def get_bishop_or_rook_moves(self, row, col, valid_move_set, rook=True): 
        # logic to ensure that pinned rooks cannot move.
        piece_pinned = False
        direction = ()
        queen_check = rook and self.board[row][col][1] == 'Q'

        # go through the generated pins and check if the current piece is pinned.
        pin = None
        for pin in self.pins: 
            if pin[0] == row and pin[1] == col: 
                piece_pinned = True
                direction = (pin[2], pin[3])
                if (queen_check): 
                    break
        if pin and piece_pinned and not queen_check: self.pins.remove(pin)


        piece_colour = self.board[row][col][0]
        enemy_colour = 'w'
        if (piece_colour == enemy_colour): enemy_colour = 'b'
       
        directions = []

        if rook: directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        else: directions = [(-1, -1), (1, -1), (-1, 1), (1, 1)]

        # for each direction, we need to compute all the possible directions, holding 7 squares in any direction as the maximum.
        # at any time, any piece that can move distances across the board, can move atmost 7 squares in any one directions.
        # we use the second for loop for this purpose and the first loop to iterate over each possible direction for the rook.
        # after we get all the possible moves, we can filter these moves to ensure that only the valid ones are returned.

        for dr in directions: 
            for i in range(1, len(self.board)): 

                # to explain the math here, we are calculating the ending row by adding the product of the 
                # number of steps to take in this specific iteration in which specific direction to the 
                # current row and column value.

                end_row = row + (dr[0] * i)
                end_col = col + (dr[1] * i)

                
                # if the end_row and end_col are within the bounds of the board, then this move is possibly valid.
                if (end_row < len(self.board) and end_row >= 0 and end_col < len(self.board) and end_col >= 0): 

                    if not piece_pinned or direction == dr or direction == (-dr[0], -dr[1]): 

                    # now, we need to check if a piece is sitting on the position that we are supposedly moving to.
                        end_pos = self.board[end_row][end_col]

                        if (end_pos != '--' and end_pos[0] == enemy_colour): 

                        # if we encounter an enemy piece in this direction and with so many steps, 
                        # then we will consider this move valid, but we will inspect other directions 
                        # after we add this move to the set of all valid moves. We do this because we don't
                        # want to jump enemy pieces by inspecting further moves in this same direction.

                        # Furthermore, we will also need to check if this enemy piece if a king, because 
                        # a king cannot be captured by another piece. 

                            valid_move_set.add(Move((row, col), (end_row, end_col), self.board))
                            break

                    # empty positions are always valid moves (if we are not jumping over a piece).
                        elif (end_pos == '--'):
                            valid_move_set.add(Move((row, col), (end_row, end_col), self.board))

                    # we encounter a king or a friendly piece -- look in another direction.
                        else: 
                            break

                # we have gone off-board. There is no need to look in this direction anymore -- look in another direction.
                else: 
                    break
    
    # General function to generate valid king or knight moves just like as done above for bishop or rook moves.
    def get_king_or_knight_moves(self, row, col, valid_move_set, king=True): 

        piece_colour = self.board[row][col][0]
        enemy_colour = 'w'
        if (piece_colour == enemy_colour): enemy_colour = 'b'

        if king: directions = [(-1, -1), (1, -1), (-1, 1), (1, 1), (1, 0), (0, 1), (-1, 0), (0, -1)]
        else: directions = [(-1, -2), (1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1)]

        # search for knight pins.
        if not king: 
            piece_pinned = False
            direction = ()

            # go through the generated pins and check if the current piece is pinned.
            pin = None
            for pin in self.pins: 
                if pin[0] == row and pin[1] == col: 
                    piece_pinned = True
                    break
            if pin and piece_pinned: self.pins.remove(pin)


        for dr in directions: 
            end_row = row + dr[0]
            end_col = col + dr[1]

            if (end_row < len(self.board) and end_row >= 0 and end_col < len(self.board) and end_col >= 0):

                end_pos = self.board[end_row][end_col]

                # checking for knight pins.
                if (not king and not piece_pinned): 

                    if (end_pos != '--' and end_pos[0] == enemy_colour): 
                        valid_move_set.add(Move((row, col), (end_row, end_col), self.board))
                        
                    elif (end_pos == '--'):
                        valid_move_set.add(Move((row, col), (end_row, end_col), self.board))
                
                # checking for valid king moves that don't result in a check. That is, the king cannot make a move that puts itself into a check.
                elif king: 

                    if end_pos[0] != piece_colour: 

                        if piece_colour == 'w': self.white_king_pos = (end_row, end_col)
                        else: self.black_king_pos = (end_row, end_col)

                        self.find_pins_and_checks()

                        if not self.in_check: 
                            valid_move_set.add(Move((row, col), (end_row, end_col), self.board))

                        if piece_colour == 'w': self.white_king_pos = (row, col)
                        else: self.black_king_pos = (row, col)

                        self.find_pins_and_checks()
    
    def get_castle_moves(self, row, col, valid_move_set): 
        # if we are already in check, then we cannot castle.
        ks_castles, qs_castles = None, None

        if self.in_check: 
            return None

        if (self.white_to_move and self.current_castling_check.wks) or (not self.white_to_move and self.current_castling_check.bks):
            ks_castles = self.get_kingside_castles(row, col, valid_move_set)

        if (self.white_to_move and self.current_castling_check.wqs) or (not self.white_to_move and self.current_castling_check.bqs):
            qs_castles = self.get_queenside_castles(row, col, valid_move_set)
        
        if (ks_castles and len(ks_castles) > 0): 
            valid_move_set = valid_move_set.union(ks_castles)
        if (qs_castles and len(qs_castles) > 0):
            valid_move_set = valid_move_set.union(qs_castles)
        
        return valid_move_set


    def get_kingside_castles(self, row, col, valid_move_set): 
        set_to_return = set()
        # Note that we will only call this and the get queenside castles functions if the white king hasn't been moved
        # As such, we do not need a check for that in the functions.
        if self.board[row][col+1] == '--' and self.board[row][col+2] == '--': 
            if not self.cell_under_attack(row, col+1) and not self.cell_under_attack(row, col+2): 
                set_to_return.add(Move((row, col), (row, col+2), self.board, castling_move=True))

        return set_to_return


    def get_queenside_castles(self, row, col, valid_move_set):
        set_to_return = set()

        if self.board[row][col - 1] == '--' and self.board[row][col - 2] == '--' and self.board[row][col - 3] == '--': 
            if not self.cell_under_attack(row, col-1) and not self.cell_under_attack(row, col-2): 
                set_to_return.add(Move((row, col), (row, col-2), self.board, castling_move=True))
        return set_to_return


    # Expensive operation. Use it wisely.
    # Find if a specific cell is under attack. Used to check if the adjacent cells to a king's home position are under attack or not for castling.
    def cell_under_attack(self, row, col): 

        to_return = False
        piece_colour = 'b'

        if self.white_to_move: 
            piece_colour = 'w'
        
        if (row < len(self.board) and row >= 0 and col < len(self.board) and col >= 0):

            end_pos = self.board[row][col]

            if end_pos[0] != piece_colour:

                if piece_colour == 'w': self.white_king_pos = (row, col)
                else: self.black_king_pos = (row, col)

                self.find_pins_and_checks()

                if self.in_check: 
                    to_return = True

                if piece_colour == 'w': self.white_king_pos = (row, col)
                else: self.black_king_pos = (row, col)

                self.find_pins_and_checks()

        return to_return
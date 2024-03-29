from copy import deepcopy
from collections import deque

ROW_TO_RANKS = {7:"1", 6:"2", 5:"3", 4:"4", 3:"4", 2:"6", 1:"7", 0:"8"}
COLS_TO_FILES = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}


class Move(): 
    '''
    Represents a move made on the chess board.

    Args:
        start (tuple): Tuple representing the starting position of the piece to be moved.
        end (tuple): Tuple representing the ending position of the piece to be moved.
        board (list): A list representing the chess board.
        castling_move (bool): A boolean variable indicating whether the move was a castling move.

    Attributes:
        start_row (int): The row of the starting position of the piece to be moved.
        start_col (int): The column of the starting position of the piece to be moved.
        end_row (int): The row of the ending position of the piece to be moved.
        end_col (int): The column of the ending position of the piece to be moved.
        piece_captured (str): A string representing the piece that was captured by the move, if any.
        piece_moved (str): A string representing the piece that was moved.
        castling_move (bool): A boolean indicating whether the move was a castling move.
        id: An integer representing the unique ID of the move.
    
    Returns:
        A Move object.

    The Move class represents a move made on the chess board. The class has attributes to represent the starting position, ending position, 
    piece moved, piece captured (if any), and whether the move was a castling move or not. The class also has methods to create a unique hash value 
    for each move and to check if two moves are equal. 
    '''
    def __init__(self, start, end, board, castling_move=False): 
        self.start_row = start[0]
        self.start_col = start[1]
        self.end_row = end[0]
        self.end_col = end[1]
        self.piece_captured = board[self.end_row][self.end_col]
        self.piece_moved = board[self.start_row][self.start_col]
        self.castling_move = castling_move
        self.id = self.__hash__()

    def __hash__(self):
        return hash(self.key())
    
    def key(self): 
        return (self.start_row, self.start_col, self.end_row, self.end_col, self.piece_captured, self.piece_moved, self.castling_move)

    def __eq__(self, other):
        if isinstance(other, Move):
            return (self.start_row, self.start_col, self.end_row, self.end_col, self.piece_captured, self.piece_moved, self.castling_move) == (other.start_row, other.start_col, other.end_row, other.end_col, other.piece_captured, other.piece_moved, other.castling_move)
        return False

    def __repr__(self): 
        return  COLS_TO_FILES[self.start_col] + ROW_TO_RANKS[self.start_row] + COLS_TO_FILES[self.end_col] + ROW_TO_RANKS[self.end_row]


class CastleCheck(): 
    '''
    Class to maintain the state of castles in the chess game.
    
    Attributes:
    - wks (bool): True if the white king can still make a kingside castle, False otherwise.
    - bks (bool): True if the black king can still make a kingside castle, False otherwise.
    - wqs (bool): True if the white king can still make a queenside castle, False otherwise.
    - bqs (bool): True if the black king can still make a queenside castle, False otherwise.
    
    The class represents the state of the castling rules in the game. Castling can be done only under specific circumstances, 
    so it is necessary to keep track of the castling options available to both players. The four attributes of the class 
    indicate whether each of the four castling options (white/black kingside/queenside) is available. Each attribute is set 
    to True initially, and will be updated as castling moves are made, or if a rook or king is moved or captured.
    '''
    def __init__(self, wks, bks, wqs, bqs): 
        self.bqs = bqs
        self.bks = bks
        self.wqs = wqs
        self.wks = wks

        
class Game():
    '''
    This class defines and records the state of the chess game being played.

    Attributes:
    - board (list): The chess board.
    - white_to_move (bool): A variable that checks if it is white's turn to move or not.
    - move_log (deque): A move log, registering all the moves that occurred in the game.
    - move_functions (dict): Dictionary for function calls for more elegant code.
    - white_king_pos (tuple): Current position of the white king on the board.
    - black_king_pos (tuple): Current position of the black king on the board.
    - in_check (bool): A variable to determine if the player is currently in check or not.
    - check_mate (bool): A variable to determine if a checkmate has occurred or not.
    - stale_mate (bool): A variable to determine if a stalemate has occurred or not.
    - pins (list): A list of the pieces that are pinned.
    - checks (list): A list of the positions where the opponent has a piece that is checking the player's king.
    - current_castling_check (obj): A variable to determine if any castling rule has been broken.
    - castling_check_log (deque): A variable to keep track of the moves that affect castling rules.
    '''

    def __init__(self): 
        """
        Initializes a new instance of the Game class with the chess board, move log, and various other attributes.
        """
        # The chess board. 
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

    def make_move(self, move): 
        '''
        Makes a move on the chess board and updates the board, move log, king position, and castling moves.

        Args:
            move (Move): A Move object representing the move to be made.

        Returns:
            None.

        The function takes in a Move object and updates the chess board, move log, king position, and castling moves according to the specified move.
        If the piece being moved is not a king, it updates the square the piece was moved to with the piece symbol and sets the original square to empty.
        The function then appends the move to the move log and changes the turn to the opposite player.
        If the piece being moved is a king, it updates the king position for the corresponding player.
        If the move is a castling move, it updates the appropriate squares for the rook and king.
        Finally, it updates the castling checks and appends the current castling state to the castling check log.
        '''
        if move.piece_moved != None:
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

    def undo_move(self): 
        """
        Reverts the last move made in the game by updating the board, current turn, and castling rights.

        Args:
            self (obj): An instance of the Game class.

        Returns:
            None

        The function pops the last move object from the move log and uses it to undo the move on the board. The piece that was moved is placed back to its 
        initial position, and the piece that was captured (if any) is restored to the end square. The function also updates the king position, turn 
        status, and castling rights. Finally, the function resets any possible checkmate or stalemate flags.
        """
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

            # anytime we undo move, we can't possibly be in checkmate or stalemate.
            self.check_mate = False
            self.stale_mate = False
 
    def get_all_moves(self):
        """
        Returns a set of all possible moves on the chess board, without considering any checks.

        Args:
            self (obj): An instance of the Game class.

        Returns:
            A set of Move objects. Each Move object represents a valid move on the board.

        The function returns a set of all possible moves on the board without considering any checks. It first determines the king's position and 
        initializes an empty set to hold all possible moves. Then it loops through the entire board and finds all pieces of the player whose turn it is 
        and calls the appropriate method to compute their valid moves. The function then returns the set of all possible moves, including castling 
        moves if possible.
        """
        if self.white_to_move: 
            king_row, king_col = self.white_king_pos
        else: 
            king_row, king_col = self.black_king_pos

        all_moves = set()

        for i in range(len(self.board)): 
            for j in range(len(self.board[i])): 
                
                piece = self.board[i][j]
                
                if piece != '--' and ((piece[0] == 'w' and self.white_to_move) or (piece[0] == 'b' and not self.white_to_move)): 
                    self.move_functions[piece[1]](i, j, all_moves)
        
        return self.get_castle_moves(king_row, king_col, all_moves)
                    
    def get_valid_moves(self): 
        """
        Returns a set of all possible valid moves on the chess board, considering checks.

        Args:
            self (obj): An instance of the Game class.

        Returns:
            A set of Move objects. Each Move object represents a valid move on the board.

        The function returns a set of all possible valid moves on the board, considering checks. It first initializes an empty set of valid moves 
        and a set of valid cells. Then it calls the 'find_pins_and_checks' method to determine if the king is in check and to identify any pins or 
        checks on the board. If the king is not in check, then all moves should be valid except for those that result in the king being in check. 
        In this case, the function calls the 'get_all_moves' method to obtain all possible moves and returns the set. If the king is in check, then 
        the function performs additional checks to filter out invalid moves. If the king is checked in only one way, then the function either moves 
        the king or blocks the check. If the attacker is a knight, then only the king or the knight can move to block the check. If the attacker is not 
        a knight, then the function checks for possible moves to block the check, either by moving a piece in the direction of the attack or by capturing 
        the attacking piece. The function then filters all valid moves such that only the moves that end up in the valid cells remain. If the king is 
        checked in multiple ways, then the function returns all possible moves of the king. The function sets the 'check_mate' flag to True if the king 
        is in checkmate or 'state_mate' flag to True if the game is in a stalemate. The function then returns the set of valid moves.
        """
        valid_moves = set()
        valid_cells = set()
        self.find_pins_and_checks()

        if self.white_to_move: 
            king_row, king_col = self.white_king_pos
        else: 
            king_row, king_col = self.black_king_pos
        
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
                else: 
                    self.state_mate = True

            else: 
                # need this in case we undo we need to reset any checkmates or statemates.
                self.check_mate = False
                self.state_mate = False

        else: 
            # if the king is not in check, then all moves should be valid, minus the ones that directly lead to the king being in check, i.e. pins.
            return self.get_all_moves()

        return valid_moves
    
    def get_capture_moves(self):
        """
        Returns a list of all capture moves on the chess board.

        Args:
            self(obj): An instance of the Game class.

        Returns:
            A list of Move objects. Each Move object represents a capture move on the board.

        The function returns a list of all capture moves on the board. It first gets all valid moves using the 'get_valid_moves' method. 
        Then it iterates over every move and checks if the end position of the move has a piece on it or not. If there is a piece on the end 
        position, the move is a capture move, and it is added to the list of capture moves. The function then returns the list of capture moves.
        """
        capture_moves = []
        all_moves = self.get_valid_moves()

        for move in all_moves:
            if self.board[move.end_row][move.end_col] != "--":
                capture_moves.append(move)

        return capture_moves

    def update_castle_check(self, move): 
        """
        Updates the current castling check object with the new castling rights after a move is made.

        Args:
            move (Move): An instance of the Move class representing the move that was made.

        Returns:
            None. The method updates the relevant castling rights of the current_castling_check object.

        The function updates the current_castling_check object to reflect the new castling rights after a move is made. 
        If the king or rook is moved, the corresponding castling right is removed. If a rook is captured, the corresponding 
        castling right is removed. The current_castling_check object stores the current castling rights and is used to check 
        if a player can castle on their turn. 
        """
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
        '''
        Finds all possible pins and checks on a chess board for the current player.

        For knights, the function iterates over every possible knight move from the king's location, checking for a check.

        Args:
            self(obj): An instance of the Game class.

        Returns:
            None. The function updates the 'in_check', 'pins', and 'checks' instance variables with the calculated values.
        
        The function determines whose turn it is, what the player color is, what the opponent color is, and where the player's king is located.
        Then it checks every possible direction that can produce a check, looking for possible pins or checks. For each direction, 
        the function iterates over every cell in that direction, checking if there is a pin or a check. If there is a pin, the function 
        adds it to the list of pins, and if there is a check, it adds it to the list of checks. If an attacker in a direction cannot produce a check, 
        the function does not check this direction further. If there is an attacker in a direction that can produce a check, the function checks 
        whether there is a pin or not. If there is no pin, the function adds the check to the list of checks. If there is a pin, it adds the pin to the list of pins.
        '''
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

    ###############################################
    ### FUNCTIONS TO GET MOVES OF DIFFERENT PIECES.
    ###############################################
    def get_pawn_moves(self, row, col, valid_move_set): 
        """
        Generates all possible valid moves for a pawn piece on a chess board.

        Args:
            - row (int): the row index of the piece on the board.
            - col (int): the column index of the piece on the board.
            - valid_move_set (set): a set to hold all the possible valid moves.

        Returns:
            None. The function adds all possible valid moves to the valid_move_set set parameter.

        The function first checks if the pawn is pinned, meaning it cannot move because it would expose the king.
        If it is white's turn, the function computes the valid moves of the white pawns, considering empty squares and captures.
        If it is black's turn, the function computes the valid moves of the black pawns, considering empty squares and captures.
        Valid moves are added to the valid_move_set set parameter.
        """
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
        """
        Generates all possible valid moves for a rook piece on a chess board.

        Args:
            - row (int): the row index of the piece on the board.
            - col (int): the column index of the piece on the board.
            - valid_move_set (set): a set to hold all the possible valid moves.

        Returns:
            None. The function adds all possible valid moves to the valid_move_set set parameter.

        Calls the 'get_bishop_or_rook_moves' function with the 'rook' parameter set to True.
        """
        self.get_bishop_or_rook_moves(row, col, valid_move_set)

    def get_knight_moves(self, row, col, valid_move_set):
        """
        Generates all possible valid moves for a knight piece on a chess board.

        Args:
            - row (int): the row index of the piece on the board.
            - col (int): the column index of the piece on the board.
            - valid_move_set (set): a set to hold all the possible valid moves.

        Returns:
            None. The function adds all possible valid moves to the valid_move_set set parameter.

        Calls the 'get_king_or_knight_moves' function with the 'king' parameter set to False.
        """
        self.get_king_or_knight_moves(row, col, valid_move_set, king=False)

    def get_bishop_moves(self, row, col, valid_move_set): 
        """
        Generates all possible valid moves for a bishop piece on a chess board.

        Args:
            - row (int): the row index of the piece on the board.
            - col (int): the column index of the piece on the board.
            - valid_move_set (set): a set to hold all the possible valid moves.

        Returns:
            None. The function adds all possible valid moves to the valid_move_set set parameter.

        Calls the 'get_bishop_or_rook_moves' function with the 'rook' parameter set to False.
        """
        self.get_bishop_or_rook_moves(row, col, valid_move_set, rook=False)

    def get_king_moves(self, row, col, valid_move_set): 
        """
        Generates all possible valid moves for a king piece on a chess board.

        Args:
            - row (int): the row index of the piece on the board.
            - col (int): the column index of the piece on the board.
            - valid_move_set (set): a set to hold all the possible valid moves.

        Returns:
            None. The function adds all possible valid moves to the valid_move_set set parameter.

        Calls the 'get_king_or_knight_moves' function with the 'king' parameter set to True.
        """
        self.get_king_or_knight_moves(row, col, valid_move_set, king=True)

    def get_queen_moves(self, row, col, valid_move_set): 
        """
        Generates all possible valid moves for a queen piece on a chess board.

        Args:
            - row (int): the row index of the piece on the board.
            - col (int): the column index of the piece on the board.
            - valid_move_set (set): a set to hold all the possible valid moves.

        Returns:
            None. The function adds all possible valid moves to the valid_move_set set parameter.

        Calls the 'get_bishop_or_rook_moves' function twice - first with the 'rook' 
        parameter set to True and then with it set to False. This is done because the queen 
        moves like the bishop mixed in with the rook.
        """
        self.get_bishop_or_rook_moves(row, col, valid_move_set, rook=True)
        self.get_bishop_or_rook_moves(row, col, valid_move_set, rook=False)


    # Since both bishops and rooks follow the same algorithm to compute valid moves, for the sake of simplicity of design, we will design a generic function
    # that is controlled by a flag variable indicating whether is the bishop or the rook's moves which need to be computed. 
    def get_bishop_or_rook_moves(self, row, col, valid_move_set, rook=True): 
        '''
        This function generates all possible valid moves for a bishop or a rook piece on a chess board.

        Args:
        - row (int): the row index of the piece on the board.
        - col (int): the column index of the piece on the board.
        - valid_move_set (set): a set to hold all the possible valid moves.
        - rook (bool, optional): a boolean value indicating whether the piece is a rook or a bishop.
        Default is True, indicating the piece is a rook.

        Returns:
        None. The function adds all possible valid moves to the valid_move_set set parameter.

        The function first checks if the piece is pinned, meaning it cannot move because it would expose the king.
        It then determines the color of the piece, and the direction(s) it can move in. Using a nested for loop, the function
        generates all the possible moves the piece can make. The function also checks if the move is valid by checking if the
        piece is moving onto an empty square, capturing an opponent piece or moving off the board. The valid moves are added
        to the valid_move_set set parameter
        '''
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

                        if (end_pos != '--' and end_pos[0] == enemy_colour and end_pos[1] != 'K'): 

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
    
    def get_king_or_knight_moves(self, row, col, valid_move_set, king=True): 
        '''
        Generates valid moves for a king or a knight at a given position.

        Args:
            row (int): The row index of the piece.
            col (int): The column index of the piece.
            valid_move_set (set): The set of valid moves for the piece.
            king (bool): Whether the piece is a king (True) or a knight (False).

        Returns:
            None

        This function generates valid moves for a king or a knight at the specified position (row, col). 
        If king is True, it generates all valid moves for a king, excluding moves that would put the king into check. 
        If king is False, it generates all valid moves for a knight, and checks for any pins on the piece.
        The generated moves are added to the valid_move_set.
        '''
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

                    if (end_pos != '--' and end_pos[0] == enemy_colour and end_pos[1] != 'K'): 
                        valid_move_set.add(Move((row, col), (end_row, end_col), self.board))
                        
                    elif (end_pos == '--'):
                        valid_move_set.add(Move((row, col), (end_row, end_col), self.board))
                
                # checking for valid king moves that don't result in a check. That is, the king cannot make a move that puts itself into a check.
                elif king: 

                    if end_pos[0] != piece_colour and end_pos[1] != 'K': 

                        if piece_colour == 'w': self.white_king_pos = (end_row, end_col)
                        else: self.black_king_pos = (end_row, end_col)

                        self.find_pins_and_checks()

                        if not self.in_check: 
                            valid_move_set.add(Move((row, col), (end_row, end_col), self.board))

                        if piece_colour == 'w': self.white_king_pos = (row, col)
                        else: self.black_king_pos = (row, col)

                        self.find_pins_and_checks()
    
    def get_castle_moves(self, row, col, valid_move_set): 
        """
        Returns a set of valid move objects that include the possible castle moves for the king at the given position.
        A castle move can be either kingside or queenside, and requires that the king and the rook involved in the castling
        have not moved before, and that the squares between them are unoccupied and not under attack.
            
        Parameters:
            row (int): The row index of the king's position on the board.
            col (int): The column index of the king's position on the board.
            valid_move_set (set): A set of valid move objects for the king piece at the given position.
            
        Returns:
            set: A set of valid move objects that include the possible castle moves for the king at the given position.
        """
        ks_castles, qs_castles = None, None

        if self.in_check: 
            return valid_move_set

        if (self.white_to_move and self.current_castling_check.wks) or (not self.white_to_move and self.current_castling_check.bks):
            ks_castles = self.get_kingside_castles(row, col)

        if (self.white_to_move and self.current_castling_check.wqs) or (not self.white_to_move and self.current_castling_check.bqs):
            qs_castles = self.get_queenside_castles(row, col)
        
        if (ks_castles and len(ks_castles) > 0): 
            valid_move_set = valid_move_set.union(ks_castles)

        if (qs_castles and len(qs_castles) > 0):
            valid_move_set = valid_move_set.union(qs_castles)

        return valid_move_set

    def get_kingside_castles(self, row, col): 
        """
        Given a row and column corresponding to the position of a king,
        returns a set of legal moves corresponding to kingside castling if it is a legal move.

        Args:
            row (int): The row of the king.
            col (int): The column of the king.

        Returns:
            set: A set of legal moves corresponding to kingside castling, represented as Move objects,
            or an empty set if kingside castling is not legal.
        """
        set_to_return = set()
        if self.board[row][col+1] == '--' and self.board[row][col+2] == '--': 
            if not self.cell_under_attack(row, col+1) and not self.cell_under_attack(row, col+2): 
                set_to_return.add(Move((row, col), (row, col+2), self.board, castling_move=True))

        return set_to_return

    def get_queenside_castles(self, row, col):
        set_to_return = set()

        if self.board[row][col-1] == '--' and self.board[row][col-2] == '--' and self.board[row][col-3] == '--': 
            if not self.cell_under_attack(row, col-1) and not self.cell_under_attack(row, col-2): 
                set_to_return.add(Move((row, col), (row, col-2), self.board, castling_move=True))
        return set_to_return

    def cell_under_attack(self, row, col): 
        """
        Determines whether the cell at the given position on the board is being attacked by any of the opponent's pieces.
        
        Args:
        - row (int): The row of the cell being checked.
        - col (int): The column of the cell being checked.
        
        Returns:
        - A boolean value indicating whether the cell is under attack by any of the opponent's pieces.
        
        This function checks whether the cell at the given position on the board is being attacked by any of the opponent's
        pieces. It does so by temporarily moving the king of the current player to the cell, and then checking whether the king
        is in check. If the king is in check, then the cell is under attack.
        
        Note that this function only works if the positions of the kings on the board are known, so the find_kings() function
        should be called before calling this function for the first time.
        """
        to_return = False
        piece_colour = 'b'
        start_pos = self.black_king_pos

        if self.white_to_move: 
            piece_colour = 'w'
            start_pos = self.white_king_pos

        
        if (row < len(self.board) and row >= 0 and col < len(self.board) and col >= 0):

            end_pos = self.board[row][col]

            if end_pos[0] != piece_colour:

                if piece_colour == 'w': 
                    self.white_king_pos = (row, col)
                else: 
                    self.black_king_pos = (row, col)

                self.find_pins_and_checks()

                if self.in_check: 
                    to_return = True

                if piece_colour == 'w': 
                    self.white_king_pos = start_pos
                else: 
                    self.black_king_pos = start_pos

                self.find_pins_and_checks()

        return to_return
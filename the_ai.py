### MODULE THAT HANDLES AI RESPONSIBILITIES.
import random 

# our algorithm to make the AI pick a good move will involve implementing the minimax algo -- a process which leads
# to select the move the creates the "best" game state for the respective player: black or white.
# we need a heuristic function -- a way to quantify how "good" a game state is for a player.
# to get the heuristic, we'll create a dictionary to assign a "score" to each piece and to each resulting game state.

# we will treat the algorithm with the zero-sum concept, so that if white is winning our total board "score" will be positive
# but if black is winning our total board "score" will be negative. This way the two opposing colours will be trying to 
# maximize and minimize at the same time. 

PIECE_SCORE = {"K": 0, "Q": 10, "R": 5, "B": 3, "K": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0


### Function to generate random move for the AI
def find_random_move(valid_move_set): 
    valid_move_list = list(valid_move_set)
    return valid_move_list[random.randint(0, len(valid_move_list)-1)]


### Function to generate a "good" move for the AI based on an implementation of the minmax algorithm.
def find_good_move(game, valid_move_set):

    best_move = None
    white_or_black = False

    if (game.white_to_move): 
        white_or_black = True

    if not white_or_black: 
        # greedy algo on moves for black.
        min_score = CHECKMATE
        for move in valid_move_set:

            game.make_move(move)

            if game.check_mate: 
                curr_score = -CHECKMATE
            elif game.stale_mate: 
                curr_score = STALEMATE
            else: 
                curr_score = score_board(game.board)

            curr_score = score_board(game.board)
            if (curr_score < min_score): 
                min_score = curr_score
                best_move = move
            
            game.undo_move()
    else: 
        # greedy algo on moves for white.
        max_score = -CHECKMATE

        for move in valid_move_set:

            game.make_move(move)

            if game.check_mate: 
                curr_score = CHECKMATE
            elif game.stale_mate: 
                curr_score = STALEMATE
            else: 
                curr_score = score_board(game.board)

            if (curr_score > max_score): 
                max_score = curr_score
                best_move = move
            
            game.undo_move()

    return best_move

    
### Function to score the board based on our piece mapping created earlier. This function defines the heuristic of our algorithm.
def score_board(board): 

    total_score = 0

    for row in board: 
        for col in row: 
            # zero-sum concept applied here. Black subtracts and white adds.
            if (col[0] == 'w'): 
                total_score += PIECE_SCORE.get(col[1], 0)
            elif (col[0] == 'b'): 
                total_score -= PIECE_SCORE.get(col[1], 0)

    return total_score
    



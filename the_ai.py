### MODULE THAT HANDLES AI RESPONSIBILITIES.
import random 

# our algorithm to make the AI pick a good move will involve implementing the minimax algo -- a process which leads
# to select the move the creates the "best" game state for the respective player: black or white.
# we need a heuristic function -- a way to quantify how "good" a game state is for a player.
# to get the heuristic, we'll create a dictionary to assign a "score" to each piece and to each resulting game state.

# we will treat the algorithm with the zero-sum concept, so that if white is winning our total board "score" will be positive
# but if black is winning our total board "score" will be negative. This way the two opposing colours will be trying to 
# maximize and minimize at the same time. 

# since the minmax algo by itself is very inefficient, as we will be computing redundant maxes and minimums, we will be using
# alpha-beta pruning, a concept to store the best move of the maximizing player (the A.I.) and the best move of the minimizing 
# player (the human). Thus, if we encounter a branch of decisions that seem like they cannot lead to a better result that our
# current best moves, then we do not inspect that branch any further and thus "prune" it.

PIECE_SCORE = {"K": 0, "Q": 10, "R": 5, "B": 3, "K": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0

# for depth of the game tree -- essentially, how many moves the AI will look forward.
DEPTH = 2

### Function to generate random move for the AI
def find_random_move(valid_move_set): 
    valid_move_list = list(valid_move_set)
    return valid_move_list[random.randint(0, len(valid_move_list)-1)]


# ### Function to generate a "good" move for the AI based on an implementation of the minmax algorithm. This follows a greedy algo.
# def find_good_move(game, valid_move_set):

#     best_move = None
#     white_or_black = False

#     if (game.white_to_move): 
#         white_or_black = True

#     if not white_or_black: 
#         # greedy algo on moves for black.
#         min_score = CHECKMATE
#         for move in valid_move_set:

#             game.make_move(move)

#             if game.check_mate: 
#                 curr_score = -CHECKMATE
#             elif game.stale_mate: 
#                 curr_score = STALEMATE
#             else: 
#                 curr_score = score_board(game)

#             curr_score = score_board(game)
#             if (curr_score < min_score): 
#                 min_score = curr_score
#                 best_move = move
            
#             game.undo_move()
#     else: 
#         # greedy algo on moves for white.
#         max_score = -CHECKMATE

#         for move in valid_move_set:

#             game.make_move(move)

#             if game.check_mate: 
#                 curr_score = CHECKMATE
#             elif game.stale_mate: 
#                 curr_score = STALEMATE
#             else: 
#                 curr_score = score_board(game)

#             if (curr_score > max_score): 
#                 max_score = curr_score
#                 best_move = move
            
#             game.undo_move()

#     return best_move

### Function to generate a "better" move for the AI based on an implementation of the minmax algorithm. This follows the recursive version of the minmax algorithm.
def find_move_minmax(game, valid_move_set, depth, maximizing_player): 
    # base case.
    if depth == 0: 
        return score_board(game)
    

### Helper function for find_better_move function to be called in the main. 
def find_better_move(game, valid_move_set): 
    global AI_move
    AI_move = None
    find_move_minmax(game, valid_move_set, DEPTH, game.white_to_move)
    return AI_move

### Function to score the board based on our piece mapping created earlier. This function defines the heuristic of our algorithm.
def score_board(game): 

    total_score = 0
    
    # if the maximizing player perceives a checkmate in the future, they should work towards it.
    # same concept with the mimizing player. 
    # this is why we set the value of the checkmate so high. 
    # note the turns are flipped because a checkmate will switch turns from the winner to the loser. 
    if game.check_mate: 
        if game.white_to_move: 
            return -CHECKMATE
        else: 
            return CHECKMATE
    
    # if the player perceives a stalemate, they would prefer that over a losing position, so the value has been set to 0.
    # 0 indicates indifference for both maximizing and minimizing players.
    elif game.stale_mate: 
        return STALEMATE

    for row in game.board: 
        for col in row: 
            # zero-sum concept applied here. Black wants to minimize the score by subtracting and white wants to maximize the score by adding.
            if (col[0] == 'w'): 
                total_score += PIECE_SCORE.get(col[1], 0)
            elif (col[0] == 'b'): 
                total_score -= PIECE_SCORE.get(col[1], 0)

    return total_score
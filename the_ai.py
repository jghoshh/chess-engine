### MODULE THAT HANDLES AI RESPONSIBILITIES.
import random 
from functools import cache, lru_cache

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
CHECKMATE = 10000
STALEMATE = 0

# for depth of the game tree -- essentially, how many moves the AI will look forward.
DEPTH = 3

### Function to generate random move for the AI
def find_random_move(valid_move_set): 
    valid_move_list = list(valid_move_set)
    return valid_move_list[random.randint(0, len(valid_move_list)-1)]

### Public function for the min max algo to be called from the main. 
def find_good_move(game, valid_move_set): 
    AI_move = [None]

    ### Function to generate a "better" move for the AI based on an implementation of the minmax algorithm. This follows the recursive version of the minmax algorithm.
    ### Currently, the function is inefficient, but once alpha-beta pruning is implemented the function will run a lot faster. 
    def find_move_minmax(valid_move_set, depth, alpha, beta, maximizing_player): 
    # base case is if we have looked as many moves as possible ahead, as specified by the depth parameter.
        if depth == 0: 
            return score_board(game)
    
        # If it is currently the maximizing player's turn, then we will need to recurse down and back up the 
        # game tree with respect to the depth parameter to find the current move that has the best chance 
        # of maximizing our score in the future. We thus set max_score to the worst possible score we 
        # could get as the maximizing player and iterate and recurse through all our possible current moves.
        # once we hit the depth of the game tree, we will recurse back up to the initial call of this function
        # and while doing so will have accounted for the maximum possible score that we could attain.
        # This score will consequently determine what move we should play currently to be able to attain this
        # maximized score in the future.
        #
        # Note that when we recurse up and down the game tree, we will not only need to calculate our 
        # maximizing moves, but also the minimizing moves of our opponent, as they will try to take
        # away as much as possible from our score. To predict moves into the future, we cannot only 
        # consider our moves in a two player game. 
        if maximizing_player: 
            max_score = -CHECKMATE
            for move in valid_move_set:
                game.make_move(move)
                next_possible_moves = game.get_valid_moves()
                curr_score = find_move_minmax(next_possible_moves, depth-1, not maximizing_player)
                if curr_score > max_score: 
                    max_score = curr_score
                    if depth == DEPTH: 
                        AI_move[0] = move
                game.undo_move()
                
                #alpha-beta pruning
                alpha = max(alpha, max_score)
                # if our opponent's best move so far is less than our best move,
                # then we don't need to inspect any other valid moves, because
                # our opponent will not less us cast this move. 
                if beta <= alpha: 
                    break

            return max_score

        else: 
            min_score = CHECKMATE
            for move in valid_move_set:
                game.make_move(move)
                next_possible_moves = game.get_valid_moves()
                curr_score = find_move_minmax(next_possible_moves, depth-1, not maximizing_player)
                if curr_score < min_score: 
                    min_score = curr_score
                    if depth == DEPTH: 
                        AI_move[0] = move
                game.undo_move()

                #alpha-beta pruning
                beta = min(beta, max_score)
                # if our opponent's best move so far is better than our best move,
                # then we don't need to inspect any other valid moves, because
                # our opponent will not less us cast this move. 
                if beta <= alpha: 
                    break

            return min_score

    find_move_minmax(valid_move_set, DEPTH, -CHECKMATE, CHECKMATE, game.white_to_move)
    return AI_move[0]

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
### MAIN MODULE RESPONSIBLE FOR HANDLING USER INPUT AND RUNNING THE CHESS GAME.
import pygame 
import engine
from the_ai import find_random_move, find_good_move
from move import Move

pygame.init()
WIDTH = HEIGHT = 512
DIM = 8
SQ_SIZE = HEIGHT // DIM
MAX_FPS = 15
IMGS = {}
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Chess Engine Demo")

### Function to load in images. Note that we only want to do this operation once, as it is quite expensive.
def load_images(board): 
    for row in board: 
        for col in row: 
            if col != "--": 
                # We are storing the images alongisde its supposed size in the board.
                IMGS[col] = pygame.transform.smoothscale(pygame.image.load(f"images/{col}.png"), (SQ_SIZE, SQ_SIZE))


### Function to draw the board and pieces.
def draw_board(surface, game): 
    light = (254, 203, 153) 
    dark = (204, 152, 102)
    curr = light

    for i in range(DIM): 
        for j in range(DIM):
            piece = game.board[i][j]
            pygame.draw.rect(surface, curr, pygame.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            if j != DIM - 1: 
                if (curr == light): curr = dark
                else: curr = light
            if piece != '--': 
                surface.blit(IMGS[piece], pygame.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_result(surface, prompt): 
    font = pygame.font.Font("./font/NunitoSans-Black.ttf", 22)
    text_object = font.render(prompt, 0, pygame.Color('Black'))
    location = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - text_object.get_width()/2, HEIGHT/2 - text_object.get_height()/2)
    surface.blit(text_object, location)

### Main function to run the game.
def main():  
    game = engine.Game()
    valid_moves = game.get_valid_moves()
    load_images(game.board)
    run = True

    # Flag variable to ensure that the expensive operation of generate valid moves is not done every frame. 
    move_made = False

    # we need to store two positions of where the user clicked: one click to select the piece, one click to select the position to move the piece to.
    player_clicks = [] # this list will store the two clicks of the user in the form of two tuples. 

    # the current cell that is selected -- used for highlighting purposes.
    cell_selected = ()

    # need a two variables to denote which position the AI will be playing and which position the player will be playing.
    # whatever colour human plays is white, and whatever colour the AI plays will be black.
    white = True
    black = False
    undo = False
    game_over = False

    while run: 
        # to check if it is the human's turn.
        human = (game.white_to_move and white) or (not game.white_to_move and black)

        for event in pygame.event.get(): 

            if event.type == pygame.QUIT:
                run = False

            # Key press handlers. 
            elif event.type == pygame.KEYDOWN: 
                # Looking out for presses in the 'z' key.
                if event.key == pygame.K_z:
                    game.undo_move()
                    move_made = True                   
                
                # Looking out for presses in the 'r' key.
                if event.key == pygame.K_r:
                    game = engine.Game()
                    valid_moves = game.get_valid_moves()
                    player_clicks.clear()
                    game_over = False

            # Mouse button handlers.
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                #first, get the matrix-indexed format of the position that the user clicked.
                if human and not game_over: 
                    x, y = pygame.mouse.get_pos()
                    col = x//SQ_SIZE 
                    row = y//SQ_SIZE
                    cell_selected = (row, col)

                    #if the user clicked the same square twice, then we will clear the click stack and undo the player's selection of a piece.
                    if player_clicks and player_clicks[0] == (row, col):
                        player_clicks.clear()
                    else: 
                        #if the click is on a unique square, then we store it in the click stack.
                        player_clicks.append((row, col)) 

                    #if two clicks have been recognized, then we validate and make the move defined by the two clicks.
                    if (len(player_clicks) == 2):

                        curr_move = None
                        first_click_pos = game.board[player_clicks[0][0]][player_clicks[0][1]]
                        second_click_pos = game.board[player_clicks[1][0]][player_clicks[1][1]]
                        
                        if (not first_click_pos == '--' or not second_click_pos == '--'): 

                            curr_move = Move(player_clicks[0], player_clicks[1], game.board)

                            if curr_move.piece_moved[1] == 'K' and (abs(curr_move.end_col - curr_move.start_col) == 2) and (curr_move.start_row == curr_move.end_row): 
                                curr_move.castling_move = True

                            if curr_move and curr_move in valid_moves: 
                                #we have to make it a castling move.
                                game.make_move(curr_move)
                                if game.move_log: print(game.move_log[-1])
                                move_made = True

                        player_clicks.clear()
        
        if move_made: 
            valid_moves = game.get_valid_moves()
            move_made = False

        # AI move making. 
        if not human and not game_over:
            AI_move = find_good_move(game, valid_moves)
            print(AI_move)
            if not AI_move: 
                AI_move = find_random_move(valid_moves)
            game.make_move(AI_move)
            if game.move_log: print(game.move_log[-1])
            move_made = True

        draw_board(WINDOW, game)
        
        stale_mate_check = len(game.move_log) >= 8 and (game.move_log[-1] == game.move_log[-5]) and (game.move_log[-2] and game.move_log[-6]) and (game.move_log[-3] and game.move_log[-7]) and (game.move_log[-4] and game.move_log[-8])
        if game.stale_mate or stale_mate_check:
            draw_result(WINDOW, "Stalemate. 'R' to play again.")
            game_over = True

        elif game.check_mate:
            if game.white_to_move: 
                draw_result(WINDOW, "Black wins by checkmate! 'R' to play again.")
                game_over = True
            else: 
                draw_result(WINDOW, "White wins by checkmate! 'R' to play again.")
                game_over = True

        CLOCK.tick(MAX_FPS)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__": 
    main()
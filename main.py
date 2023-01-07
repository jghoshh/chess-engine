### MAIN MODULE RESPONSIBLE FOR HANDLING USER INPUT AND RUNNING THE CHESS GAME.
import pygame 
import engine
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


### bug in this function. Not worth the time to fix.
### Function to highlight the initial square selected and all valid moves given a piece.
# def highlight(surface, game, valid_move_set, selected_cell): 

#     if selected_cell: 
#         row, col = selected_cell

#         if (game.white_to_move and game.board[row][col][0] == 'w') or (not game.white_to_move and game.board[row][col][0] == 'b'): 
            
#             # prepare and draw the blue highlight on the selected square.
#             s = pygame.Surface((SQ_SIZE, SQ_SIZE))
#             s.set_alpha(10)
#             s.fill(pygame.Color('blue'))
#             surface.blit(s, (col*SQ_SIZE, row*SQ_SIZE))
            
#             # prepare the surface for yellow highlights on valid_moves.
#             s.fill(pygame.Color('yellow'))

#             # draw the yellow highlights on the valid moves. 
#             for move in valid_move_set: 
#                 if move.start_row == row and move.start_col == col: 
#                     surface.blit(s, (move.end_col * SQ_SIZE, move.end_row * SQ_SIZE))


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

    while run: 

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

            # Mouse button handlers.
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                #first, get the matrix-indexed format of the position that the user clicked.
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

        draw_board(WINDOW, game)

        if game.stale_mate:
            draw_result(WINDOW, "Stalemate. 'R' to play again.")

        elif game.check_mate:
            if game.white_to_move: 
                draw_result(WINDOW, "Black wins by checkmate! 'R' to play again.")
            else: 
                draw_result(WINDOW, "White wins by checkmate! 'R' to play again.")

        CLOCK.tick(MAX_FPS)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__": 
    main()
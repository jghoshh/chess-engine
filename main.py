### MAIN MODULE RESPONSIBLE FOR HANDLING USER INPUT AND RUNNING THE CHESS GAME.
import pygame 
import engine
import move

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

### Function to draw the game, board, and pieces.
def draw_game(surface, game):
    draw_board(surface, game.board)


def draw_board(surface, board): 
    light = (207, 167, 110) 
    dark = (107, 37, 4)

    curr = light
    count = 0
    for i in range(DIM): 
        for j in range(DIM):
            piece = board[i][j]
            pygame.draw.rect(surface, curr, pygame.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            if j != DIM - 1: 
                if (curr == light): curr = dark
                else: curr = light
            if piece != '--': 
                surface.blit(IMGS[piece], pygame.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
# def draw_pieces(surface, board): 
#     for i in range(DIM): 
#         for j in range(DIM): 
#             piece = board[i][j]
#             if piece != '--': 
#                 surface.blit(IMGS[piece], pygame.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))

### Main function to run the game.
def main(): 
    game = engine.Game()
    load_images(game.board)
    run = True

    # we need to store two positions of where the user clicked: one click to select the piece, one click to select the position to move the piece to.
    player_clicks = [] # this list will store the two clicks of the user in the form of two tuples. 

    while run: 

        for event in pygame.event.get(): 

            if event.type == pygame.QUIT:
                run = False

            # Key press handlers. 
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_z: # Looking out for presses in the 'z' key.
                    game.undo_move()
            
            # Mouse button handlers.
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                #first, get the matrix-indexed format of the position that the user clicked.
                x, y = pygame.mouse.get_pos()
                col = x//SQ_SIZE 
                row = y//SQ_SIZE

                #if the user clicked the same square twice, then we will clear the click stack and undo the player's selection of a piece.
                if player_clicks and player_clicks[0] == (row, col):
                    player_clicks.clear()
                else: 
                    #if the click is on a unique square, then we store it in the click stack.
                    player_clicks.append((row, col)) 

                #if two clicks have been recognized, then we validate and make the move defined by the two clicks.
                if (len(player_clicks) == 2):
                    game.validate_and_move(player_clicks[0], player_clicks[1])
                    if (game.move_log): print(move.convert_to_c(game.move_log[-1]))
                    player_clicks.clear()

        draw_game(WINDOW, game)

        CLOCK.tick(MAX_FPS)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__": 
    main()
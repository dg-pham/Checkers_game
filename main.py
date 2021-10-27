# from AI import minimax
from constants import *
from game import Game
from utils import blit_text_center

# font
pygame.font.init()
MAIN_FONT = pygame.font.SysFont('comicsans', 44)

# load & scale images
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('checker')


# funtions
def get_index_from_mouse(pos):
    x, y = pos
    # return row, col of the selected piece
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


# variables
run = True
clock = pygame.time.Clock()
FPS = 60
game = Game(WIN)

# run game
while run:
    # compute how many milliseconds have passed since the previous call
    clock.tick(FPS)

    # # AI
    # if game.turn == WHITE:
    #     value, new_board = minimax(game.get_board(), 4, WHITE, game)
    #     game.ai_move(new_board)

    # game over
    if game.winner() is not None:
        blit_text_center(WIN, MAIN_FONT, f'{game.winner()} won the game!')
        pygame.display.update()
        # wait 5s before game restart
        pygame.time.wait(5000)
        game.reset()

    # draw board
    game.update()

    # game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # get position by click
            pos = pygame.mouse.get_pos()
            row, col = get_index_from_mouse(pos)
            # play!
            game.select(row, col)

            # # if no one can move
            # piece = game.board.get_piece(row, col)
            # if piece != 0 and piece.color == game.turn:
            #     if game.board.get_valid_moves(piece) is None:
            #         blit_text_center(WIN, MAIN_FONT, f'{game.turn} won the game!')
            #         pygame.display.update()
            #         # wait 5s before game restart
            #         pygame.time.wait(5000)
            #         game.reset()
# exit game
pygame.quit()

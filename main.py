from constants import *

from game import Game

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

    # game over
    if game.winner() is not None:
        print(game.winner())
        run = False

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

# exit game
pygame.quit()

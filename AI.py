from copy import deepcopy

import pygame.draw

from constants import WHITE, RED, GREEN


def simulate_move(piece, move, board, skip):
    # move
    board.move(piece, move[0], move[1])
    # skip
    if skip:
        board.remove(skip)
    # get each simulated board
    return board


def get_all_moves(board, color, game):
    moves = []
    for piece in board.get_all_pieces(color):
        # get all valid moves
        valid_moves = board.get_valid_moves(piece)
        # consider all moves
        for move, skip in valid_moves.items():
            # draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, skip)
            moves.append(new_board)

    # get all results
    return moves


# the main algorithm
def minimax(board, depth, to_maximize, game):
    # when depth == 0 return the evaluated board
    if depth == 0 or board.winner() is not None:
        return board.evaluate(), board

    # the AI needs to maximize scores of White side
    if to_maximize:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(board, WHITE, game):
            # AI need to minimize scores of Red side
            evaluation = minimax(move, depth - 1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            # pick the best moves
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move

    # next consider, AI need to minimize scores of Red side, so let to_maximize = False
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(board, RED, game):
            # next consider, AI need to minimize scores of Red side, so let to_maximize = False
            evaluation = minimax(move, depth - 1, True, game)[0]
            minEval = min(minEval, evaluation)
            # pick the best moves
            if minEval == evaluation:
                best_move = move

        return minEval, best_move


# check AI algorithm
def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, GREEN, (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(100)

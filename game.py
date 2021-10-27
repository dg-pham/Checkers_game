import pygame.display

from board import Board
from constants import RED, WHITE, BLUE, SQUARE_SIZE


class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        # draw board
        self.board.draw(self.win)
        # draw valid moves
        self.draw_valid_moves(self.valid_moves)
        # update
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        # apply winner for current board
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        # try moving a piece
        if self.selected:
            result = self._move(row, col)
            # if invalid, reset select() function
            if not result:
                self.selected = None
                self.select(row, col)

        # select a piece and get all of its valid moves
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        if self.selected and (row, col) in self.valid_moves:
            # move
            self.board.move(self.selected, row, col)
            # skip
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            # change turn
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(
                self.win,
                BLUE,
                (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                15
            )

    def change_turn(self):
        # remove when done
        self.valid_moves = {}
        # change turn
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        # get current board
        return self.board

    def ai_move(self, board):
        # change board
        self.board = board
        # change turn
        self.change_turn()

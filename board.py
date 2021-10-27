import pygame.draw

from constants import BLACK, ROWS, SQUARE_SIZE, RED, COLS, WHITE
from piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            # alternating (red, black) squares
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        # swap (row, col) of selected piece and (row, col) of where moved
        self.board[piece.row][piece.col], self.board[row][col] \
            = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        # king piece conditions
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def evaluate(self):
        # get scores of current board situation
        return self.white_left - self.red_left + (self.white_kings * 1.5 - self.red_kings * 1.5)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        # get all current side's pieces to evaluate
        return pieces

    def get_piece(self, row, col):
        # return piece in (row, col) (= 0 if does not have)
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            # append board[row]
            self.board.append([])

            for col in range(COLS):
                # each row appends piece
                if col % 2 == (row + 1) % 2:
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        # temporary
                        self.board[row].append(0)
                else:
                    # temporary
                    self.board[row].append(0)

    def draw(self, win):
        # draw squares
        self.draw_squares(win)
        # draw pieces
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            # remove in board
            self.board[piece.row][piece.col] = 0
            # remove in list
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return 'White'
        elif self.white_left <= 0:
            return 'Red'
        # haven't end yet
        return None

    def get_valid_moves(self, piece):
        # dictionary contains all valid moves of a current position
        moves = {}
        # check situation
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        # red go up and white go down
        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        # # debug
        # print(moves)

        # return all moves and skipped pieces (if has)
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        if skipped is None:
            skipped = []
        moves = {}
        # piece which is skipped to move
        last = []
        for r in range(start, stop, step):
            # out of board
            if left < 0:
                break

            # consider a left square
            current = self.board[r][left]
            # if current is an empty square
            if current == 0:
                # if skipped the piece and have not seen a piece yet
                if skipped and not last:
                    break
                # if skipped a piece
                elif skipped:
                    moves[(r, left)] = last + skipped
                # if couldn't skip, just move normally
                else:
                    moves[(r, left)] = last

                # if last existed
                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    # check for potential multiple skip (after skipped a last, update function for new loop)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            # if current is an ally
            elif current.color == color:
                break
            # if current is an enemy
            else:
                last = [current]
            # update left for new loop
            left -= 1

        # return all left and skipped pieces (if has)
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        if skipped is None:
            skipped = []
        moves = {}
        last = []
        for r in range(start, stop, step):
            # out of board
            if right >= COLS:
                break

            # consider a right square
            current = self.board[r][right]
            # if current is an empty square
            if current == 0:
                # if skipped the piece and have not seen a piece yet
                if skipped and not last:
                    break
                # if skipped a piece
                elif skipped:
                    moves[(r, right)] = last + skipped
                # if couldn't skip, just move normally
                else:
                    moves[(r, right)] = last

                # if last existed
                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    # check for potential multiple skip (after skipped a last, update function for new loop)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            # if current is an ally
            elif current.color == color:
                break
            # if current is an enemy
            else:
                last = [current]
            # update right for new loop
            right += 1

        # return all right and skipped pieces (if has)
        return moves

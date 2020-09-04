import math
import random
import copy

class AI:
    def __init__(self):
        self.EMPTY = 0
        self.AI_PIECE = 2
        self.PLAYER_PIECE = 1
        self.window_length = 5

    def winning_move(self, board, piece):
        # check horizontal locations for win
        for m in range(len(board)):
            for n in range(len(board) - 4):
                if board[m][n] == piece and board[m][n + 1] == piece and board[m][n + 2] == piece and \
                   board[m][n + 3] == piece and board[m][n + 4] == piece:
                   return True
        # check vertical lovcations for win
        for m in range(len(board) - 4):
            for n in range(len(board)):
                if board[m][n] == piece and board[m + 1][n] == piece and board[m + 2][n] == piece and \
                   board[m + 3][n] == piece and board[m + 4][n] == piece:
                   return True
        # check diagonal locations for win
        for m in range(len(board) - 4):
            for n in range(len(board) - 4):
                if board[m][n] == piece and board[m + 1][n + 1] == piece and board[m + 2][n + 2] == piece and \
                   board[m + 3][n + 3] == piece and board[m + 4][n + 4] == piece:
                   return True
        for m in range(len(board) - 4):
            for n in range(len(board) - 4):
                if board[len(board) - m - 1][n] == piece and board[len(board) - m - 2][n + 1] == piece and board[len(board) - m - 3][n + 2] == piece and \
                   board[len(board) - m - 4][n + 3] == piece and board[len(board) - m - 5][n + 4] == piece:
                   return True

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = self.PLAYER_PIECE
        if piece == self.PLAYER_PIECE:
            opp_piece = self.AI_PIECE
        if window.count(piece) == 5:
            score += 100
        elif window.count(piece) == 4 and window.count(self.EMPTY) == 1:
            score += 10
        elif window.count(piece) == 3 and window.count(self.EMPTY) == 2:
            score += 5
        if window.count(piece) == 2 and window.count(self.EMPTY) == 3 and window[window.index(piece) + 1] == piece:
            score += 2
        if window.count(opp_piece) == 4 and window.count(self.EMPTY) == 1:
            score -= 9
        elif window.count(opp_piece) == 3 and window.count(self.EMPTY) == 2:
            score -= 4
        if window[0] == self.PLAYER_PIECE and window[1] == self.AI_PIECE and window[2] == self.AI_PIECE:
            score -= 3
        if window[0] == self.AI_PIECE and window[1] == self.PLAYER_PIECE and window[2] == self.PLAYER_PIECE:
            score += 5
        return score

    def heuristic(self, board, piece):
        score = 0
        # horizontal score
        for m in range(len(board)):
            for n in range(len(board) - 4):
                window = [board[m][n], board[m][n + 1], board[m][n + 2], board[m][n + 3], board[m][n + 4]]
                score += self.evaluate_window(window, piece)
        # vertical score
        for m in range(len(board) - 4):
            for n in range(len(board)):
                window = [board[m][n], board[m + 1][n], board[m + 2][n], board[m + 3][n], board[m + 4][n]]
                score += self.evaluate_window(window, piece)
        # diagonal score
        for m in range(len(board) - 4):
            for n in range(len(board) - 4):
                window = [board[m][n], board[m + 1][n + 1], board[m + 2][n + 2], board[m + 3][n + 3], board[m + 4][n + 4]]
                score += self.evaluate_window(window, piece)
        for m in range(len(board) - 4):
            for n in range(len(board) - 4):
                window = [board[len(board) - m - 1][n], board[len(board) - m - 2][n + 1], \
                          board[len(board) - m - 3][n + 2], board[len(board) - m - 4][n + 3], board[len(board) - m - 5][n + 4]]
                score += self.evaluate_window(board, piece)
        return score

    def is_terminal_node(self, board):
        checks = [self.winning_move(board, self.PLAYER_PIECE), self.winning_move(board, self.AI_PIECE)]
        return any(checks) or len(self.get_valid_locations(board)) == 0

    def get_valid_locations(self, board):
        valid_locations = []
        for m in range(len(board)):
            for n in range(len(board[m])):
                if board[n][m] == 0:
                    valid_locations.append((m, n))
        return valid_locations

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        is_terminal = self.is_terminal_node(board)
        valid_locations = self.get_valid_locations(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(board, self.AI_PIECE):
                    return (None, None), 10 ** 10
                if self.winning_move(board, self.PLAYER_PIECE):
                    return (None, None), - 10 ** 10
                else: return (None, None), 0
            else: return (None, None), self.heuristic(board, self.AI_PIECE)
        if maximizingPlayer:
            value = - math.inf
            (m, n) = random.choice(valid_locations)
            for (x, y) in valid_locations:
                board_copy = copy.deepcopy(board)
                board_copy[y][x] = self.AI_PIECE
                new_score = self.minimax(board_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    (m, n) = (x, y)
                alpha = max(alpha, value)
                if alpha >= beta: break
            return (m, n), value
        else:
            value = math.inf
            (m, n) = random.choice(valid_locations)
            for (x, y) in valid_locations:
                board_copy = copy.deepcopy(board)
                board_copy[y][x] = self.PLAYER_PIECE
                new_score = self.minimax(board_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    (m, n) = (x, y)
                beta = min(beta, value)
                if alpha >= beta: break
            return (m, n), value

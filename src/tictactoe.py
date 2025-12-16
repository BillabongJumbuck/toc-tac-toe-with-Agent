import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.winner = None
        self.ended = False
        self.num_players = 2
        self.current_player = 1  # 1 starts

    def reset(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.winner = None
        self.ended = False
        self.current_player = 1
        return self.get_state()

    def get_state(self):
        # Return a hashable representation of the state (tuple of tuples)
        # 0: empty, 1: player 1 (Agent), -1: player 2 (Opponent)
        return str(self.board.reshape(9))

    def get_available_moves(self):
        if self.ended:
            return []
        return list(zip(*np.where(self.board == 0)))

    def make_move(self, position):
        if self.ended:
            return False
        
        if self.board[position] != 0:
            return False

        self.board[position] = self.current_player
        
        # Check for winner
        if self.check_winner(self.current_player):
            self.winner = self.current_player
            self.ended = True
        elif np.all(self.board != 0):
            self.winner = 0  # Draw
            self.ended = True
        else:
            self.current_player = -1 if self.current_player == 1 else 1
        
        return True

    def check_winner(self, player):
        # Check rows, cols, diagonals
        for i in range(3):
            if np.all(self.board[i, :] == player) or np.all(self.board[:, i] == player):
                return True
        if np.diag(self.board).sum() == player * 3 or np.diag(np.fliplr(self.board)).sum() == player * 3:
            return True
        return False

    def is_ended(self):
        return self.ended

    def get_winner(self):
        return self.winner

    def print_board(self):
        symbols = {0: ' ', 1: 'X', -1: 'O'}
        print("-------------")
        for i in range(3):
            row = "| "
            for j in range(3):
                row += symbols[self.board[i, j]] + " | "
            print(row)
            print("-------------")

class TicTacToe:
    def __init__(self):
        self.board = [[0, 0, 0] for _ in range(3)]
        self.winner = None
        self.ended = False
        self.num_players = 2
        self.current_player = 1  # 1 starts

    def reset(self):
        self.board = [[0, 0, 0] for _ in range(3)]
        self.winner = None
        self.ended = False
        self.current_player = 1
        return self.get_state()

    def get_state(self):
        # Return a hashable representation of the state
        # Flatten the board
        flat_board = [cell for row in self.board for cell in row]
        return str(flat_board)

    def get_available_moves(self):
        if self.ended:
            return []
        moves = []
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == 0:
                    moves.append((r, c))
        return moves

    def make_move(self, position):
        if self.ended:
            return False
        
        r, c = position
        if self.board[r][c] != 0:
            return False

        self.board[r][c] = self.current_player
        
        # Check for winner
        if self.check_winner(self.current_player):
            self.winner = self.current_player
            self.ended = True
        elif self.is_full():
            self.winner = 0  # Draw
            self.ended = True
        else:
            self.current_player = -1 if self.current_player == 1 else 1
        
        return True

    def is_full(self):
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return False
        return True

    def check_winner(self, player):
        # Check rows
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                return True
        # Check cols
        for j in range(3):
            if all(self.board[i][j] == player for i in range(3)):
                return True
        # Check diagonals
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2-i] == player for i in range(3)):
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
                row += symbols[self.board[i][j]] + " | "
            print(row)
            print("-------------")

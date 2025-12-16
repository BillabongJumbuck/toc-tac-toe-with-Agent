import pickle
import os
import random

class TDAgent:
    def __init__(self, alpha=0.1, epsilon=0.1, gamma=0.9):
        self.V = {}  # Value function table: state_hash -> value
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.prev_state = None
        self.prev_action = None

    def get_value(self, state):
        if state not in self.V:
            self.V[state] = 0.5  # Initialize with 0.5 (neutral)
        return self.V[state]

    def update_value(self, state, reward, next_state=None):
        """
        TD(0) update: V(s) = V(s) + alpha * (reward + gamma * V(s') - V(s))
        """
        current_val = self.get_value(state)
        
        if next_state is None:
            target = reward
        else:
            target = reward + self.gamma * self.get_value(next_state)
            
        self.V[state] = current_val + self.alpha * (target - current_val)

    def choose_action(self, env, state, is_training=True, player=1):
        available_moves = env.get_available_moves()
        if not available_moves:
            return None

        # Epsilon-greedy
        if is_training and random.random() < self.epsilon:
            return random.choice(available_moves)

        # Greedy action based on V(s')
        best_value = -float('inf')
        best_move = available_moves[0]

        # We need to peek at the next state for each action to decide
        # env.board is a list of lists [[...], [...], [...]]
        
        # Deep copy the board manually
        current_board = [row[:] for row in env.board]
        
        for move in available_moves:
            r, c = move
            # Simulate move
            # Create a temporary board for this move
            temp_board = [row[:] for row in current_board]
            temp_board[r][c] = player # Place the piece for the current player
            
            # If we are playing as -1 (Player 2), we need to invert the board 
            # to match the perspective the agent was trained on (Agent is 1).
            if player == -1:
                check_board = [[cell * -1 for cell in row] for row in temp_board]
            else:
                check_board = temp_board
            
            # Flatten and stringify to match tictactoe.py get_state()
            flat_board = [cell for row in check_board for cell in row]
            next_state_hash = str(flat_board)
            
            val = self.get_value(next_state_hash)
            if val > best_value:
                best_value = val
                best_move = move
            elif val == best_value:
                # Randomly break ties to avoid deterministic loops in self-play
                if random.random() < 0.5:
                    best_move = move
                
        return best_move

    def save_policy(self, filename='policy.pkl'):
        with open(filename, 'wb') as f:
            pickle.dump(self.V, f)
        print(f"Policy saved to {filename}")

    def load_policy(self, filename='policy.pkl'):
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.V = pickle.load(f)
            print(f"Policy loaded from {filename}")
        else:
            print("Policy file not found, starting fresh.")

class RandomAgent:
    def choose_action(self, env):
        available_moves = env.get_available_moves()
        if not available_moves:
            return None
        return random.choice(available_moves)

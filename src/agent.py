import numpy as np
import pickle
import os

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
        For Tic-Tac-Toe, rewards usually come at the end, so intermediate rewards are 0.
        If next_state is None (terminal), V(s') is 0.
        """
        current_val = self.get_value(state)
        
        if next_state is None:
            target = reward
        else:
            target = reward + self.gamma * self.get_value(next_state)
            
        self.V[state] = current_val + self.alpha * (target - current_val)

    def choose_action(self, env, state, is_training=True):
        available_moves = env.get_available_moves()
        if not available_moves:
            return None

        # Epsilon-greedy
        if is_training and np.random.rand() < self.epsilon:
            idx = np.random.choice(len(available_moves))
            return available_moves[idx]

        # Greedy action based on V(s')
        best_value = -float('inf')
        best_move = available_moves[0]

        # We need to peek at the next state for each action to decide
        # Since we can't easily "peek" without modifying the env, we might need a helper
        # or we simulate the move.
        # A simple way is to simulate the board state string.
        
        # Let's parse the state string back to board or use the env to simulate if possible.
        # Since env.board is mutable, we should be careful. 
        # Better approach: The agent knows it's player 1.
        
        current_board = env.board.copy()
        
        for move in available_moves:
            # Simulate move
            temp_board = current_board.copy()
            temp_board[move] = 1 # Agent is always 1 in its own view for value estimation
            next_state_hash = str(temp_board.reshape(9))
            
            val = self.get_value(next_state_hash)
            if val > best_value:
                best_value = val
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
        idx = np.random.choice(len(available_moves))
        return available_moves[idx]

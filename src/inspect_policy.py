import pickle
import numpy as np
import sys
import os

def inspect_policy(policy_path='policy.pkl', output_file='policy_values.txt'):
    if not os.path.exists(policy_path):
        print(f"Policy file {policy_path} not found.")
        return

    with open(policy_path, 'rb') as f:
        V = pickle.load(f)

    print(f"Loaded policy with {len(V)} states.")
    
    # Sort by value, descending
    sorted_items = sorted(V.items(), key=lambda item: item[1], reverse=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Total States: {len(V)}\n")
        f.write("========================================\n\n")
        
        for state_str, value in sorted_items:
            # Parse state string back to board
            # state_str is like "[0 1 -1 ...]"
            try:
                # Remove brackets and convert to numpy array
                clean_str = state_str.replace('[', '').replace(']', '')
                board_flat = np.fromstring(clean_str, sep=' ', dtype=int)
                board = board_flat.reshape(3, 3)
                
                f.write(f"Value: {value:.4f}\n")
                
                # Draw board
                symbols = {0: '.', 1: 'X', -1: 'O'}
                for i in range(3):
                    row_str = " "
                    for j in range(3):
                        row_str += symbols[board[i, j]] + " "
                    f.write(row_str + "\n")
                f.write("\n----------------------------------------\n")
            except Exception as e:
                f.write(f"Error parsing state: {state_str}\nValue: {value}\nError: {e}\n\n")

    print(f"Policy values have been written to {output_file}")

if __name__ == "__main__":
    inspect_policy()

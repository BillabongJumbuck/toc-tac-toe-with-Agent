import os
import random
from tictactoe import TicTacToe
from agent import TDAgent, RandomAgent

def get_agent_state_hash(env, player):
    """
    Returns the state hash from the agent's perspective.
    If agent is Player 1 (1), returns standard hash.
    If agent is Player 2 (-1), returns hash of inverted board (so agent looks like 1).
    """
    # env.board is list of lists
    board = [row[:] for row in env.board]
    
    if player == -1:
        board = [[cell * -1 for cell in row] for row in board]
        
    flat_board = [cell for row in board for cell in row]
    return str(flat_board)

def train(episodes=20000, save_path='policy.pkl'):
    env = TicTacToe()
    agent = TDAgent(epsilon=0.1) 
    opponent = RandomAgent()
    
    print(f"Training for {episodes} episodes...")
    
    for e in range(episodes):
        env.reset()
        
        # Randomize starting player
        # 1: Agent starts (Agent is Player 1)
        # -1: Opponent starts (Agent is Player 2)
        agent_role = 1 if random.random() < 0.5 else -1
        
        # If Agent is Player 2, Opponent moves first
        if agent_role == -1:
            opp_action = opponent.choose_action(env)
            env.make_move(opp_action)
        
        # We need to store the 'afterstate' of the agent's last move to update it later
        last_agent_afterstate = None
        
        while not env.is_ended():
            # --- Agent's Turn ---
            # Agent chooses action based on the value of the resulting afterstates
            # Note: choose_action internally handles the perspective flipping if we pass the correct player
            action = agent.choose_action(env, None, player=agent_role)
            
            if action is None: break
            
            # Create the afterstate for this action
            env.make_move(action)
            
            # Get the state hash from Agent's perspective (Self=1)
            current_agent_afterstate = get_agent_state_hash(env, agent_role)
            
            # If we had a previous move, update its value based on this new afterstate value
            if last_agent_afterstate is not None:
                agent.update_value(last_agent_afterstate, 0, current_agent_afterstate)
            
            last_agent_afterstate = current_agent_afterstate
            
            # Check if Agent won immediately
            if env.is_ended():
                reward = 0
                if env.winner == agent_role:
                    reward = 1
                elif env.winner == 0: # Draw
                    reward = 0.5 
                else:
                    reward = 0
                
                # Update the current move which led to terminal state
                agent.update_value(current_agent_afterstate, reward, None)
                break
            
            # --- Opponent's Turn ---
            opp_action = opponent.choose_action(env)
            env.make_move(opp_action)
            
            # Check if Opponent won
            if env.is_ended():
                reward = 0
                if env.winner == agent_role:
                    reward = 1
                elif env.winner == 0: # Draw
                    reward = 0.5
                else:
                    reward = 0 # Loss
                
                # The agent's last move led to a state where opponent could win/draw
                # So update the last agent afterstate towards this reward
                agent.update_value(last_agent_afterstate, reward, None)
                break
            
        if (e + 1) % 1000 == 0:
            print(f"Episode {e+1}/{episodes}")

    agent.save_policy(save_path)

def play(policy_path='policy.pkl'):
    env = TicTacToe()
    agent = TDAgent(epsilon=0) # No exploration during play
    agent.load_policy(policy_path)
    
    print("Starting Game! You are Player 2 (O). Agent is Player 1 (X).")
    state = env.reset()
    env.print_board()
    
    while not env.is_ended():
        # --- Agent's Turn ---
        print("Agent is thinking...")
        action = agent.choose_action(env, env.get_state(), is_training=False)
        env.make_move(action)
        env.print_board()
        
        if env.is_ended():
            break
            
        # --- Human's Turn ---
        valid_move = False
        while not valid_move:
            try:
                user_input = input("Enter your move (row,col) e.g. 0,0 or 1,2: ")
                parts = user_input.split(',')
                r, c = int(parts[0]), int(parts[1])
                if env.make_move((r, c)):
                    valid_move = True
                else:
                    print("Invalid move, try again.")
            except ValueError:
                print("Invalid format. Use row,col")
        
        env.print_board()
        
    winner = env.get_winner()
    if winner == 1:
        print("Agent Wins!")
    elif winner == -1:
        print("You Win!")
    else:
        print("It's a Draw!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'play':
        play()
    elif len(sys.argv) > 1:
        try:
            episodes = int(sys.argv[1])
            train(episodes=episodes)
        except ValueError:
            print(f"Invalid argument '{sys.argv[1]}'. Training with default episodes.")
            train()
    else:
        train()

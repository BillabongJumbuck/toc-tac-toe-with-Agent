# Tic-Tac-Toe Reinforcement Learning Agent

This project implements a Tic-Tac-Toe agent using Tabular Reinforcement Learning (Temporal Difference Learning). The agent learns to play by playing against a random opponent and updating its value function.

[中文文档](README_CN.md)

## Project Structure

- `src/`
  - `tictactoe.py`: The game environment logic.
  - `agent.py`: The RL agent implementation (TD Learning).
  - `main.py`: Script to train the agent and play via CLI.
  - `server.py`: Simple HTTP server for the web interface.
  - `index.html`: Frontend for playing against the agent in a browser.
- `requirements.txt`: Python dependencies.
- `policy.pkl`: Saved trained policy (generated after training).

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Train the Agent

Run the training script to let the agent play against a random bot. The agent learns to play as both Player 1 (X) and Player 2 (O). Default is 20,000 episodes.

```bash
# Train with default 20,000 episodes
python src/main.py

# Train with custom number of episodes (e.g., 50,000)
python src/main.py 50000
```
This will generate a `policy.pkl` file.

### 2. Play via Command Line

You can play against the trained agent in your terminal.

```bash
python src/main.py play
```

### 3. Play via Web Interface

Start the simple Python web server.

```bash
python src/server.py
```

Then open your browser and visit: [http://localhost:8000](http://localhost:8000). You can choose whether you want to start first (X) or let the Agent start (X).

## Algorithm Details

- **State Representation**: The board state is hashed into a string to serve as the key in the value table.
- **Update Rule**: $V(S_t) \leftarrow V(S_t) + \alpha [R_{t+1} + \gamma V(S_{t+1}) - V(S_t)]$
- **Strategy**: $\epsilon$-greedy during training, Greedy during play.

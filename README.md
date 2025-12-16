# Tic-Tac-Toe Reinforcement Learning Agent / 井字棋强化学习智能体

This project implements a Tic-Tac-Toe agent using Tabular Reinforcement Learning (Temporal Difference Learning). The agent learns to play by playing against a random opponent and updating its value function.

本项目实现了一个基于表格型强化学习（时序差分学习）的井字棋智能体。该智能体通过与随机对手对弈并更新其价值函数来学习如何下棋。

## Project Structure / 项目结构

- `src/`
  - `tictactoe.py`: The game environment logic. (游戏环境逻辑)
  - `agent.py`: The RL agent implementation (TD Learning). (强化学习智能体实现)
  - `main.py`: Script to train the agent and play via CLI. (训练脚本及命令行对弈)
  - `server.py`: Simple HTTP server for the web interface. (简单的 HTTP 后端服务器)
  - `index.html`: Frontend for playing against the agent in a browser. (浏览器对弈的前端页面)
- `requirements.txt`: Python dependencies. (Python 依赖)
- `policy.pkl`: Saved trained policy (generated after training). (训练后保存的策略文件)

## Setup / 安装

1. Install dependencies / 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

## Usage / 使用方法

### 1. Train the Agent / 训练智能体

Run the training script to let the agent play against a random bot for 20,000 episodes.
运行训练脚本，让智能体与随机机器人对弈 20,000 局。

```bash
python src/main.py
```
This will generate a `policy.pkl` file.
这将生成一个 `policy.pkl` 文件。

### 2. Play via Command Line / 命令行对弈

You can play against the trained agent in your terminal.
你可以在终端中与训练好的智能体对弈。

```bash
python src/main.py play
```

### 3. Play via Web Interface / 网页对弈

Start the simple Python web server.
启动简单的 Python Web 服务器。

```bash
python src/server.py
```

Then open your browser and visit: [http://localhost:8000](http://localhost:8000)
然后在浏览器中访问：[http://localhost:8000](http://localhost:8000)

## Algorithm Details / 算法细节

- **State Representation**: The board state is hashed into a string to serve as the key in the value table.
- **Update Rule**: $V(S_t) \leftarrow V(S_t) + \alpha [R_{t+1} + \gamma V(S_{t+1}) - V(S_t)]$
- **Strategy**: $\epsilon$-greedy during training, Greedy during play.

- **状态表示**: 棋盘状态被哈希成字符串，作为价值表中的键。
- **更新规则**: $V(S_t) \leftarrow V(S_t) + \alpha [R_{t+1} + \gamma V(S_{t+1}) - V(S_t)]$
- **策略**: 训练时使用 $\epsilon$-贪婪策略，对弈时使用贪婪策略。

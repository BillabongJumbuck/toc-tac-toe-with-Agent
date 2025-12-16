# 井字棋强化学习智能体

本项目实现了一个基于表格型强化学习（时序差分学习）的井字棋智能体。该智能体通过与随机对手对弈并更新其价值函数来学习如何下棋。

## 项目结构

- `src/`
  - `tictactoe.py`: 游戏环境逻辑
  - `agent.py`: 强化学习智能体实现 (TD Learning)
  - `main.py`: 训练脚本及命令行对弈
  - `server.py`: 简单的 HTTP 后端服务器
  - `index.html`: 浏览器对弈的前端页面
- `requirements.txt`: Python 依赖
- `policy.pkl`: 训练后保存的策略文件

## 安装

1. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

### 1. 训练智能体

运行训练脚本，让智能体与随机机器人对弈。智能体会同时学习先手（Player 1）和后手（Player 2）的策略。默认为 20,000 局。

```bash
# 使用默认的 20,000 局进行训练
python src/main.py

# 自定义训练轮次 (例如 50,000 局)
python src/main.py 50000
```
这将生成一个 `policy.pkl` 文件。

### 2. 命令行对弈

你可以在终端中与训练好的智能体对弈。

```bash
python src/main.py play
```

### 3. 网页对弈

启动简单的 Python Web 服务器。

```bash
python src/server.py
```

然后在浏览器中访问：[http://localhost:8000](http://localhost:8000)。你可以在页面上选择是你先手 (X) 还是智能体先手 (X)。

## 算法细节

- **状态表示**: 棋盘状态被哈希成字符串，作为价值表中的键。
- **更新规则**: $V(S_t) \leftarrow V(S_t) + \alpha [R_{t+1} + \gamma V(S_{t+1}) - V(S_t)]$
- **策略**: 训练时使用 $\epsilon$-贪婪策略，对弈时使用贪婪策略。

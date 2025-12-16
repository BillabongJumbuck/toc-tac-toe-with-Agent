import http.server
import socketserver
import json
import os
from tictactoe import TicTacToe
from agent import TDAgent

# Global game state
env = TicTacToe()
agent = TDAgent(epsilon=0)
POLICY_PATH = 'policy.pkl'
agent_player_id = 1 # Default agent is Player 1 (X)

# Load policy if exists
if os.path.exists(POLICY_PATH):
    agent.load_policy(POLICY_PATH)
else:
    print("Warning: Policy file not found. Agent will play randomly/untrained.")

class TicTacToeHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/api/reset':
            self.handle_reset()
        elif self.path == '/api/move':
            self.handle_move()
        else:
            self.send_error(404)

    def handle_reset(self):
        global agent_player_id
        content_length = int(self.headers['Content-Length'])
        if content_length > 0:
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            user_starts = data.get('user_starts', False)
        else:
            user_starts = False # Default: Agent starts (Agent is Player 1)

        env.reset()
        
        if user_starts:
            # User is Player 1 (X), Agent is Player 2 (O)
            agent_player_id = -1
            # Wait for user move
        else:
            # Agent is Player 1 (X), User is Player 2 (O)
            agent_player_id = 1
            # Agent moves immediately
            action = agent.choose_action(env, env.get_state(), is_training=False, player=agent_player_id)
            env.make_move(action)
        
        self.send_json_response({
            'board': env.board,
            'ended': env.is_ended(),
            'winner': env.get_winner(),
            'agent_player': agent_player_id
        })

    def handle_move(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        row = data.get('row')
        col = data.get('col')
        
        if row is None or col is None:
            self.send_error(400, "Missing row or col")
            return

        # Human move
        # Human is always the "current player" when it's their turn in the UI flow
        # But we need to ensure it's actually their turn.
        # env.current_player tracks whose turn it is (1 or -1).
        # If agent_player_id is 1, Human is -1.
        # If agent_player_id is -1, Human is 1.
        
        human_player_id = -1 * agent_player_id
        
        if env.current_player != human_player_id:
             self.send_json_response({'error': 'Not your turn'}, status=400)
             return

        success = env.make_move((row, col))
        
        if not success:
            self.send_json_response({'error': 'Invalid move'}, status=400)
            return

        # Check if game ended after human move
        if not env.is_ended():
            # Agent move
            action = agent.choose_action(env, env.get_state(), is_training=False, player=agent_player_id)
            if action:
                env.make_move(action)

        self.send_json_response({
            'board': env.board,
            'ended': env.is_ended(),
            'winner': env.get_winner(),
            'agent_player': agent_player_id
        })

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

PORT = 8000

if __name__ == "__main__":
    # Ensure we are serving from the src directory where index.html will be
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), TicTacToeHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()

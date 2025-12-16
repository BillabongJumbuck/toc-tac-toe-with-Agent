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
        env.reset()
        # Agent moves first if it's Player 1
        # In main.py we had Agent as Player 1.
        # Let's keep consistency. Agent moves immediately after reset.
        
        # Agent move
        action = agent.choose_action(env, env.get_state(), is_training=False)
        env.make_move(action)
        
        self.send_json_response({
            'board': env.board.tolist(),
            'ended': env.is_ended(),
            'winner': env.get_winner()
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

        # Human move (Player 2)
        success = env.make_move((row, col))
        
        if not success:
            self.send_json_response({'error': 'Invalid move'}, status=400)
            return

        # Check if game ended after human move
        if not env.is_ended():
            # Agent move (Player 1)
            action = agent.choose_action(env, env.get_state(), is_training=False)
            if action:
                env.make_move(action)

        self.send_json_response({
            'board': env.board.tolist(),
            'ended': env.is_ended(),
            'winner': env.get_winner()
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

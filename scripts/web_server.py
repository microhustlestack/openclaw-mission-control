#!/usr/bin/env python3
"""
OpenClaw Mission Control - Web Server
Serves the dashboard UI with API endpoints
"""

import http.server
import socketserver
import json
import subprocess
import os
from pathlib import Path

PORT = 9090
WEB_DIR = Path(__file__).parent.parent / "assets" / "web-ui"

class MissionControlHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)
    
    def do_GET(self):
        # API endpoints
        if self.path == '/api/status':
            self.send_json(self.get_status())
        elif self.path == '/api/cost':
            self.send_json(self.get_cost())
        elif self.path == '/api/agents':
            self.send_json(self.get_agents())
        else:
            # Serve static files
            if self.path == '/':
                self.path = '/index.html'
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/switch':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)
            result = self.switch_model(data.get('model', ''))
            self.send_json(result)
        else:
            self.send_error(404)
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def get_status(self):
        try:
            result = subprocess.run(
                ['openclaw', 'status', '--json'],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return {
                    'status': 'ok',
                    'model': data.get('session', {}).get('model', 'unknown'),
                    'cost': 0.00,  # Extract from data
                    'cache': 99,
                    'sessions': data.get('agents', {}).get('totalSessions', 0)
                }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
        
        return {'status': 'unknown'}
    
    def get_cost(self):
        try:
            result = subprocess.run(
                ['openclaw', 'cost', 'today'],
                capture_output=True, text=True, timeout=10
            )
            return {'cost': result.stdout.strip()}
        except:
            return {'cost': 'N/A'}
    
    def get_agents(self):
        try:
            result = subprocess.run(
                ['openclaw', 'subagents', 'list'],
                capture_output=True, text=True, timeout=10
            )
            return {'agents': result.stdout.strip()}
        except:
            return {'agents': []}
    
    def switch_model(self, model):
        try:
            result = subprocess.run(
                ['openclaw', 'model', 'set', model],
                capture_output=True, text=True, timeout=30
            )
            return {
                'success': result.returncode == 0,
                'output': result.stdout or result.stderr
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def run_server(port=PORT):
    os.chdir(WEB_DIR)
    
    with socketserver.TCPServer(("", port), MissionControlHandler) as httpd:
        print(f"🦞 Mission Control Web UI")
        print(f"   URL: http://localhost:{port}")
        print(f"   Press Ctrl+C to stop\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run_server(port)

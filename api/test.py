from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({
            'status': 'API is working!',
            'message': 'This is a test message from the Vercel serverless function.',
            'api_key_configured': bool(OPENROUTER_API_KEY)
        }).encode())


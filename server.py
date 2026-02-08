# TaskFlow Backend API

from http.server import HTTPServer, BaseHTTPRequestHandler
import json

tasks = [
    {"id": 1, "title": "Set up project", "completed": True},
    {"id": 2, "title": "Build login page", "completed": False},
    {"id": 3, "title": "Add database", "completed": False},
]

class TaskHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/tasks':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(tasks).encode())

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), TaskHandler)
    print('Server running on http://localhost:8000')
    server.serve_forever()

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from functools import partial

def create_handler(callback):
    class CallbackRequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            try:
                data = json.loads(post_data)
            except:
                data = post_data
            
            callback(data)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
    return CallbackRequestHandler

def start_receiver(callback):
    handler = create_handler(callback)
    server = HTTPServer(('localhost', 8081), handler)
    print("Receiver opened on http://localhost:8081")
    server.serve_forever()
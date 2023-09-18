from . import handler
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class HttpRequestHandler(BaseHTTPRequestHandler, handler.Handler):

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('info.html', 'rb') as file:
                self.wfile.write(file.read())
	    
        elif self.path == '/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            print("Data request")
            response = {'pm25': self.PM25.variable, 'status':self.STATUS.variable}
            self.wfile.write(json.dumps(response).encode())

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

def start_server():
    server_address = ('', 80)
    httpd = HTTPServer(server_address, HttpRequestHandler)
    print('Running HTTP server on port 80...')
    httpd.serve_forever()
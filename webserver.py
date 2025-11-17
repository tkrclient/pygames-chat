from http.server import HTTPServer, BaseHTTPRequestHandler
# Import websocket.py function here:
from websocket import websocket
import threading, os

class StaticServer(BaseHTTPRequestHandler):
    def do_GET(self):
        root = os.path.join(os.getcwd(), 'html')
        if self.path == '/':
            filename = root + '/index.html'
        else:
            filename = root + self.path

        self.send_response(200)
        if filename[-4:] == '.css':
            self.send_header('Content-type', 'text/css')
        elif filename[-5:] == '.json':
            self.send_header('Content-type', 'application/javascript')
        elif filename[-3:] == '.js':
            self.send_header('Content-type', 'application/javascript')
        elif filename[-4:] == '.ico':
            self.send_header('Content-type', 'image/x-icon')
        else:
            self.send_header('Content-type', 'text/html')
        self.end_headers()

        with open(filename, 'rb') as fh:
            html = fh.read()
        self.wfile.write(html)

def run(server_class=HTTPServer, handler_class=StaticServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port {}'.format(port))
    # Run websocket.py two lines here:
    thread = threading.Thread(target=websocket)
    thread.start()
    httpd.serve_forever()

run()



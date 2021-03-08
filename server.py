import http.server # Our http server handler for http requests
import socketserver # Establish the TCP Socket connections
import os
import webbrowser
from move_coord import cube_from_scramble
import solver
import time

PORT = 8080
 
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def set_headers(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/solve"):
            self.set_headers()

            num_move = self.path[6:]
            num_move = num_move.replace("_", " ") # replace with space
            init_cube = cube_from_scramble(num_move, numeric_scramble=True)
            solution = solver.solve(init_cube)
            solution = ",".join(map(str, solution))
            self.wfile.write(solution.encode())

with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
    print("http at port", PORT)
    # webbrowser.open_new_tab("interface/index.html")
    httpd.serve_forever()
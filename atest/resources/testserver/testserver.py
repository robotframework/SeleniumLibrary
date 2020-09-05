# Initially based on:
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/336012

import os
import sys

from http.client import HTTPConnection
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn


class StoppableHttpRequestHandler(SimpleHTTPRequestHandler):
    """http request handler with QUIT stopping the server"""

    def do_QUIT(self):
        self.send_response(200)
        self.end_headers()
        self.server.shutdown()
        self.server.server_close()

    def do_POST(self):
        self.do_GET()


class ThreadingHttpServer(ThreadingMixIn, HTTPServer):
    pass


def stop_server(port=7000):
    """send QUIT request to http server running on localhost:<port>"""
    conn = HTTPConnection("localhost:%d" % port)
    conn.request("QUIT", "/")
    conn.getresponse()


def start_server(path, port=7000):
    os.chdir(path)
    server = ThreadingHttpServer(("", port), StoppableHttpRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ["start", "stop"]:
        print("usage: %s start|stop" % sys.argv[0])
        sys.exit(1)
    if sys.argv[1] == "start":
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        start_server(path)
    else:
        stop_server()

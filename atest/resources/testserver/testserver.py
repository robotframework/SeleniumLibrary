# Initially based on:
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/336012

import argparse
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
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["start", "stop"])
    parser.add_argument("--port", default=7000, type=int)
    args = parser.parse_args()
    port = args.port
    command = args.command
    if command == "start":
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        start_server(path, port)
    else:
        stop_server(port)

# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/336012

import http.client
import http.server
import os


class StoppableHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    """http request handler with QUIT stopping the server"""

    def do_QUIT(self):
        """send 200 OK response, and set server.stop to True"""
        self.send_response(200)
        self.end_headers()
        self.server.stop = True

    def do_POST(self):
        # We could also process paremeters here using something like below.
        # length = self.headers['Content-Length']
        # print(self.rfile.read(int(length)))
        self.do_GET()


class StoppableHttpServer(http.server.HTTPServer):
    """http server that reacts to self.stop flag"""

    def serve_forever(self):
        """Handle one request at a time until stopped."""
        self.stop = False
        while not self.stop:
            self.handle_request()


def stop_server(port=7000):
    """send QUIT request to http server running on localhost:<port>"""
    conn = http.client.HTTPConnection("localhost:%d" % port)
    conn.request("QUIT", "/")
    conn.getresponse()


def start_server(port=7000):
    import os
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), '..'))
    server = StoppableHttpServer(('', port), StoppableHttpRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2 or sys.argv[1] not in ['start', 'stop']:
        print('usage: %s start|stop' % sys.argv[0])
        sys.exit(1)
    if sys.argv[1] == 'start':
        start_server()
    else:
        stop_server()

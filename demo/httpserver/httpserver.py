#  Copyright 2008-2009 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


#!/usr/bin/env python

"""Simple HTTP server requiring only Python and no other preconditions.

Server is started by running this script with argument 'start' and
optional port number (default port is defined below). Server root is
html directory in the same directory where this script is
situated. Server can be stopped either using Ctrl-C or running this
script with argument 'stop' and same port number as when starting it.

Functionality for starting and stopping using 'start' and 'stop' is
based on Active State's Python Cookbook recipe 
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/336012
"""

import SimpleHTTPServer
import BaseHTTPServer
import httplib


DEFAULT_PORT = 7272


class _StoppableHttpRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """http request handler with QUIT stopping the server"""

    def do_QUIT(self):
        """send 200 OK response, and set server.stop to True"""
        self.send_response(200)
        self.end_headers()
        self.server.stop = True

    def do_POST(self):
        # We could also process paremeters here using something like below.
        # length = self.headers['Content-Length']
        # print self.rfile.read(int(length))
        self.do_GET()


class _StoppableHttpServer(BaseHTTPServer.HTTPServer):
    """http server that reacts to self.stop flag"""

    def serve_forever(self):
        """Handle one request at a time until stopped."""
        self.stop = False
        while not self.stop:
            self.handle_request()


def start_server(port=DEFAULT_PORT):
    server = _StoppableHttpServer(('', port), _StoppableHttpRequestHandler)
    server.serve_forever()

    
def stop_server(port=DEFAULT_PORT):
    """send QUIT request to http server running on localhost:<port>"""
    conn = httplib.HTTPConnection("localhost:%d" % port)
    conn.request("QUIT", "/")
    conn.getresponse()

    
if __name__ == '__main__':
    import sys
    import os

    def process_args(args):
        if not (1 <= len(args) <= 2) or args[0] not in [ 'start', 'stop' ]:
            raise Exception
        if len(args) == 1:
            port = DEFAULT_PORT
        else:
            port = int(args[1])
        return args[0] == 'start', port

    try:
        start, port = process_args(sys.argv[1:])
    except:
        print 'usage: %s start|stop [port]' % os.path.basename(sys.argv[0])
        sys.exit(1)

    if start:
        basedir = os.path.dirname(os.path.abspath(__file__))
        htmldir = os.path.join(basedir, 'html')
        os.chdir(htmldir) 
        print "Starting demo server to port %s" % port
        start_server(port)
    else:
        print "Stopping demo server on port %s" % port
        stop_server(port)

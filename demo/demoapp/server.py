#!/usr/bin/env python

#  Copyright 2008-2010 Nokia Siemens Networks Oyj
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

"""Simple HTTP server requiring only Python and no other preconditions.

Server is started by running this script with argument 'start' and
optional port number (default port 7272). Server root is the same
directory where this script is situated. Server can be stopped either
using Ctrl-C or running this script with argument 'stop' and same port
number as when starting it.
"""

import os
import sys
import httplib
import BaseHTTPServer
import SimpleHTTPServer


DEFAULT_PORT = 7272


class StoppableHttpServer(BaseHTTPServer.HTTPServer):

    def serve_forever(self):
        self.stop = False
        while not self.stop:
            try:
                self.handle_request()
            except KeyboardInterrupt:
                break


class StoppableHttpRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_QUIT(self):
        self.send_response(200)
        self.end_headers()
        self.server.stop = True

    def do_POST(self):
        # We could also process paremeters here using something like below.
        # length = self.headers['Content-Length']
        # print self.rfile.read(int(length))
        self.do_GET()


def start_server(port=DEFAULT_PORT):
    print "Demo application starting on port %s" % port
    root  = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root) 
    server = StoppableHttpServer(('localhost', int(port)), StoppableHttpRequestHandler)
    server.serve_forever()

    
def stop_server(port=DEFAULT_PORT):
    print "Demo application on port %s stopping" % port
    conn = httplib.HTTPConnection("localhost:%s" % port)
    conn.request("QUIT", "/")
    conn.getresponse()

def print_help():
    print __doc__


if __name__ == '__main__':
    try:
        {'start': start_server,
         'stop': stop_server,
         'help': print_help}[sys.argv[1]](*sys.argv[2:])
    except (IndexError, KeyError, TypeError):
        print 'Usage: %s start|stop|help [port]' % os.path.basename(sys.argv[0])

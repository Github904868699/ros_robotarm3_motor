#!/usr/bin/env python3
import os
import rospy
from http.server import SimpleHTTPRequestHandler, HTTPServer

def main():
    rospy.init_node('web_ui_http_server')
    root = rospy.get_param('~root', os.path.join(os.path.dirname(__file__), '..', 'www'))
    port = int(rospy.get_param('~port', 8080))
    os.chdir(root)
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    rospy.loginfo('Serving %s on port %d', root, port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()

if __name__ == '__main__':
    main()

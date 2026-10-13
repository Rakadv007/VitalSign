"""
VitalSign — Web Application Server
Serves the HTML5/CSS3/JavaScript Machine Learning Dashboard via standard HTTP server.
Zero third-party dependencies required.
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = int(os.environ.get("PORT", 8000))
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)


def run_server():
    os.chdir(DIRECTORY)
    handler = CustomHTTPRequestHandler
    
    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print("=" * 60)
        print("VitalSign -- Machine Learning Healthcare Analytics Dashboard")
        print("=" * 60)
        print(f"Web Application is live at: {url}")
        print("Open the link above in your browser to view the dashboard.")
        print("Press Ctrl+C to stop the server.")
        print("=" * 60)
        
        # Open browser automatically
        try:
            webbrowser.open(url)
        except Exception:
            pass
            
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server. Goodbye!")
            sys.exit(0)


if __name__ == "__main__":
    run_server()

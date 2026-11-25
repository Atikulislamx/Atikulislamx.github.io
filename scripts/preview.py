# -*- coding: utf-8 -*-
"""Local preview server that mimics GitHub Pages with the _config.yml excludes.

    python3 scripts/preview.py [port]

Serves the repository root, resolves directory URLs to index.html, and returns
404 for build inputs and internal documents so the local preview matches what
the public site is allowed to expose.
"""
import os
import posixpath
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCKED_PREFIXES = ("/docs/", "/prompts/", "/scripts/", "/design/", "/data/", "/_source/",
                    "/assets/_source/", "/node_modules/", "/.git/")
BLOCKED_EXACT = ("/README.md", "/RELEASE.md", "/package.json", "/package-lock.json",
                 "/.env.example", "/_config.yml")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_GET(self):
        path = posixpath.normpath(self.path.split("?")[0].split("#")[0])
        if not path.startswith("/"):
            path = "/" + path
        if path.startswith(BLOCKED_PREFIXES) or path in BLOCKED_EXACT or path.endswith(".md"):
            self.send_error(404, "Not published")
            return
        super().do_GET()

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print("Serving %s on http://0.0.0.0:%d" % (ROOT, port))
    server.serve_forever()

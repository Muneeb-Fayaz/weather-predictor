"""Tiny dependency-free API + static server.
Run:  python server.py   ->  http://localhost:8000
API:  GET /api/predict?city=Jammu&days=3
"""
import json
import os
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

import predictor

PORT = int(os.environ.get("PORT", 8000))
HERE = os.path.dirname(os.path.abspath(__file__))


def load_env():
    path = os.path.join(HERE, ".env")
    if os.path.exists(path):
        for line in open(path):
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                os.environ.setdefault(k, v)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body if isinstance(body, bytes) else body.encode())

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        if u.path == "/api/predict":
            q = urllib.parse.parse_qs(u.query)
            city = q.get("city", ["Jammu"])[0]
            days = max(1, min(7, int(q.get("days", ["3"])[0])))
            try:
                self._send(200, json.dumps(predictor.run(city, days)))
            except Exception as e:
                self._send(400, json.dumps({"error": str(e)}))
        elif u.path in ("/", "/index.html"):
            self._send(200, open(os.path.join(HERE, "index.html"), "rb").read(), "text/html")
        else:
            self._send(404, json.dumps({"error": "not found"}))


if __name__ == "__main__":
    load_env()
    print(f"Weather Predictor running -> http://localhost:{PORT}")
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()

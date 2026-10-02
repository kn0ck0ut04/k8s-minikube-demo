import json
import math
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


class Handler(BaseHTTPRequestHandler):
    def _reply(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        request = urlparse(self.path)
        if request.path == "/healthz":
            return self._reply(200, {"status": "ok"})
        if request.path == "/":
            return self._reply(200, {
                "app": "my-app",
                "message": "Hello from Minikube",
                "pod": os.environ.get("HOSTNAME", "local"),
            })
        if request.path != "/work":
            return self._reply(404, {"error": "not found"})

        try:
            seconds = float(parse_qs(request.query).get("seconds", ["0.5"])[0])
        except ValueError:
            return self._reply(400, {"error": "seconds must be a number from 0.05 to 2"})
        if not math.isfinite(seconds) or not 0.05 <= seconds <= 2:
            return self._reply(400, {"error": "seconds must be a number from 0.05 to 2"})

        deadline = time.perf_counter() + seconds
        iterations = 0
        while time.perf_counter() < deadline:
            iterations += 1
        return self._reply(200, {"work_seconds": seconds, "iterations": iterations})

    def log_message(self, *_args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()

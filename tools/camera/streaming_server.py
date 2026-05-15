"""
J.A.R.V.I.S. Camera Streaming Server
Streams camera feed via HTTP for remote viewing.
"""

import threading
from typing import Optional

from jarvis_core.logger import Logger


class StreamingServer:
    def __init__(self):
        self.log = Logger("StreamingServer")
        self._server = None
        self._thread: Optional[threading.Thread] = None
        self._running = False

    def start(self, capture, port: int = 8080) -> bool:
        if self._running:
            self.log.warn("Streaming server already running.")
            return True

        try:
            from http.server import HTTPServer, BaseHTTPRequestHandler
            import cv2

            capture_ref = capture

            class StreamingHandler(BaseHTTPRequestHandler):
                def do_GET(self):
                    if self.path == "/":
                        self.send_response(200)
                        self.send_header("Content-type", "multipart/x-mixed-replace; boundary=frame")
                        self.end_headers()

                        while capture_ref._initialized:
                            frame = capture_ref.read()
                            if frame is not None:
                                _, jpeg = cv2.imencode(".jpg", frame)
                                self.wfile.write(b"--frame\r\n")
                                self.wfile.write(b"Content-Type: image/jpeg\r\n\r\n")
                                self.wfile.write(jpeg.tobytes())
                                self.wfile.write(b"\r\n")
                    else:
                        self.send_response(404)
                        self.end_headers()

            self._server = HTTPServer(("0.0.0.0", port), StreamingHandler)
            self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
            self._thread.start()
            self._running = True

            self.log.info(f"Streaming server started on port {port}")
            return True

        except Exception as e:
            self.log.error(f"Streaming server failed: {e}")
            return False

    def stop(self) -> None:
        if self._server:
            self._server.shutdown()
            self._server = None
        self._running = False
        self.log.info("Streaming server stopped.")
import json
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from . import 山彥


class 響(BaseHTTPRequestHandler):
    def do_POST(self):
        len_ = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(len_).decode('utf8')
        try:
            assert self.path == '/liber'
            if 山彥.當前山彥:
                req = json.loads(data)
                content = req.get('content', data) if isinstance(req, dict) else data
                山彥.當前山彥.讀者.動態執行(content)
                山彥.當前山彥.更新()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        except Exception as e:
            logging.exception(e)
            self.send_response(500)
            self.end_headers()


def 啓動服務(port=8000):
    server = HTTPServer(('0.0.0.0', port), 響)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    logging.info(f'監聽服務已在端口 {port} 啓動。')

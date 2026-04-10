import socket
import threading
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from protocol.message import (
    build_join,
    build_message,
    build_leave,
    encode_message,
    decode_message
)

BUFFER_SIZE = 4096


class NetworkClient:
    def __init__(self, host="127.0.0.1", port=9999):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False

    def connect(self):
        self.sock.connect((self.host, self.port))
        self.running = True
        print(f"[CLIENT] Đã kết nối tới {self.host}:{self.port}")

    def send_join(self, username):
        msg = build_join(username)
        self.sock.sendall(encode_message(msg))

    def send_message(self, username, text):
        msg = build_message(username, text)
        self.sock.sendall(encode_message(msg))

    def send_leave(self, username):
        msg = build_leave(username)
        self.sock.sendall(encode_message(msg))

    def receive_loop(self, callback):
        def run():
            buffer = ""
            while self.running:
                try:
                    data = self.sock.recv(BUFFER_SIZE)
                    if not data:
                        print("[CLIENT] Server đóng kết nối.")
                        break
                    buffer += data.decode("utf-8")

                    while "\n" in buffer:
                        raw, buffer = buffer.split("\n", 1)
                        raw = raw.strip()
                        if raw:
                            msg = decode_message(raw)
                            callback(msg)

                except Exception as e:
                    if self.running:
                        print(f"[CLIENT] Lỗi nhận: {e}")
                    break
            self.running = False

        thread = threading.Thread(target=run, daemon=True)
        thread.start()

    def close(self):
        self.running = False
        self.sock.close()

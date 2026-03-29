import socket
import threading
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from protocol.message import (
    decode_message, encode_message,
    build_message, build_leave,
    MSG_JOIN, MSG_MSG, MSG_LEAVE
)

class Chatserver:
    def __init__(self, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port
        self._clients = {}
        self._lock = threading.Lock()
        self.chat_history = []
        self.history_lock = threading.Lock()

    def start(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((self.host, self.port))
        server_sock.listen()
        print(f"Server đang chạy {self.host}:{self.port}")
        print("Chờ kết nối...")

        try:
            while True:
                client_sock, address = server_sock.accept()
                print(f"Có người kết nối từ {address}")
                t = threading.Thread(
                    target=self.handle_client,
                    args=(client_sock, address),
                    daemon=True
                )
                t.start()
        except KeyboardInterrupt:
            print("\nServer đang tắt...")
        finally:
            server_sock.close()

    def handle_client(self, client_sock: socket.socket, address):
        buffer = ''
        username = None

        try:
            while True:
                data = client_sock.recv(4096)
                if not data:
                    break

                buffer += data.decode('utf-8')

                while "\n" in buffer:
                    raw, buffer = buffer.split("\n", 1)
                    raw = raw.strip()
                    if not raw:
                        continue

                    msg = decode_message(raw)
                    msg_type = msg.get("type")

                    if msg_type == MSG_JOIN:
                        username = msg["username"]
                        with self._lock:
                            self._clients[client_sock] = username
                        print(f"[JOIN] {username} ({address})")

                    elif msg_type == MSG_MSG:
                        if username is None:
                            continue
                        print(f"[MSG] {username}: {msg['text']}")
                        self._broadcast(build_message(username, msg["text"]))

                    elif msg_type == MSG_LEAVE:
                        break

                    else:
                        print(f"[WARN] Tin nhắn lạ từ {address}: {raw}")

        except ConnectionResetError:
            print(f"[!] {address} mất kết nối đột ngột")
        except Exception as e:
            print(f"[ERROR] {address}: {e}")
        finally:
            with self._lock:
                self._clients.pop(client_sock, None)
            client_sock.close()
            if username:
                print(f"[LEAVE] {username} ({address})")
                self._broadcast(build_leave(username))

    def _broadcast(self, message: str, exclude: socket.socket = None):
        data = encode_message(message)
        with self.history_lock:
            self.chat_history.append(message)
        with self._lock:
            for sock in list(self._clients.keys()):
                if sock == exclude:
                    continue
                try:
                    sock.sendall(data)
                except Exception:
                    pass


if __name__ == "__main__":
    server = Chatserver()
    server.start()

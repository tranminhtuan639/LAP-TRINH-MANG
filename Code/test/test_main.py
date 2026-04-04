import os
import sys

# Thêm thư mục gốc vào sys.path để import client và protocol khi chạy trực tiếp
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)

from client.network import NetworkClient
from protocol.message import MSG_JOIN, MSG_MSG, MSG_LEAVE


def print_message(msg: dict) -> None:
    msg_type = msg.get("type")
    if msg_type == MSG_JOIN:
        print(f"[JOIN] {msg['username']} đã tham gia.")
    elif msg_type == MSG_MSG:
        print(f"[{msg['username']}] {msg['text']}")
    elif msg_type == MSG_LEAVE:
        print(f"[LEAVE] {msg['username']} đã rời.")
    else:
        print(f"[UNKNOWN] {msg.get('raw')}")


def main() -> None:
    print("=== Chat Client ===")
    host = input("Host (mặc định 127.0.0.1): ").strip() or "127.0.0.1"
    port_text = input("Port (mặc định 9999): ").strip() or "9999"
    username = input("Tên người dùng: ").strip()

    if not username:
        print("Tên người dùng không được để trống.")
        return

    try:
        port = int(port_text)
    except ValueError:
        print("Port không hợp lệ.")
        return

    client = NetworkClient(host=host, port=port)

    try:
        client.connect()
        client.send_join(username)
        client.receive_loop(print_message)

        print("Nhập tin nhắn. Gõ /quit để thoát.")
        while client.running:
            try:
                text = input()
            except EOFError:
                break

            if text.strip().lower() == "/quit":
                client.send_leave(username)
                break

            if text.strip():
                client.send_message(username, text)

    except Exception as exc:
        print(f"[ERROR] {exc}")
    finally:
        client.close()
        print("Đã ngắt kết nối.")


if __name__ == "__main__":
    main()

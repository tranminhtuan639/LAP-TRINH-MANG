

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.network import NetworkClient
from protocol.message import MSG_JOIN, MSG_MSG, MSG_LEAVE


def handle_message(msg: dict):
    t = msg.get("type")
    if t == MSG_JOIN:
        print(f"\n  *** {msg['username']} đã tham gia ***")
    elif t == MSG_MSG:
        print(f"\n  [{msg['username']}] {msg['text']}")
    elif t == MSG_LEAVE:
        print(f"\n  *** {msg['username']} đã rời ***")
    else:
        print(f"\n  [?] raw: {msg}")
    # In lại prompt để người dùng không bị mất dòng nhập
    print("  > ", end="", flush=True)


def main():
    username = input("Tên của mày: ").strip()
    if not username:
        username = "Anonymous"

    client = NetworkClient(host="127.0.0.1", port=9999)

    try:
        client.connect()
    except ConnectionRefusedError:
        print("[!] Không kết nối được — server đang chạy chưa?")
        sys.exit(1)

    client.send_join(username)
    client.receive_loop(handle_message)

    print(f"Xin chào {username}! Gõ tin nhắn rồi Enter. Gõ 'quit' để thoát.\n")

    try:
        while True:
            print("  > ", end="", flush=True)
            text = input()
            if text.lower() == "quit":
                break
            if text.strip():
                client.send_message(username, text)
    except KeyboardInterrupt:
        pass
    finally:
        client.send_leave(username)
        time.sleep(0.1)   # Cho server kịp nhận LEAVE trước khi đóng socket
        client.close()
        print("\n[CLIENT] Đã ngắt kết nối.")


if __name__ == "__main__":
    main()
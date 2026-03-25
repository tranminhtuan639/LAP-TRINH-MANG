import socket # Thư viện socket dùng để tạo kết nối TCP/IP
import threading # Dùng để chạy đa luồng (vừa gửi vừa nhận cùng lúc)

from protocol.message import (
    build_join,
    build_message,
    build_leave,
    encode_message,
    decode_message
)
# Import các hàm xử lý protocol (tạo message, encode, decode)

class NetworkClient: # Lớp chịu trách nhiệm giao tiếp TCP với server

    def __init__(self, host="192.168.1.19", port=9000): # Host lấy từ máy
        # Hàm khởi tạo

        self.host = host # Địa chỉ IP server (máy mà client sẽ kết nối)
        self.port = port # Cổng server đang lắng nghe
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Tạo socket TCP
        # AF_INET = IPv4
        # SOCK_STREAM = TCP (kết nối có kiểm soát, đảm bảo dữ liệu)

        self.running = False # Biến cờ để kiểm soát vòng lặp nhận dữ liệu

    def connect(self): # Kết nối tới server
        self.sock.connect((self.host, self.port)) # Mở kết nối TCP tới server (giống như gọi điện)
        self.running = True # Đánh dấu là client đang hoạt động
        print("Connected to server") # In ra để kiểm tra đã kết nối thành công

    def send_join(self, username): # Gửi message JOIN (khi user vừa vào chat)
        msg = build_join(username) # Tạo message dạng: JOIN|username
        self.sock.sendall(encode_message(msg))
        # encode → chuyển thành bytes
        # sendall → gửi toàn bộ dữ liệu qua TCP

    def send_message(self, username, text): # Gửi tin nhắn chat

        msg = build_message(username, text) # Tạo message dạng: MSG|username|text
        self.sock.sendall(encode_message(msg)) # Gửi message qua socket

    def send_leave(self, username): # Gửi message khi user rời khỏi

        msg = build_leave(username) # Tạo message dạng: LEAVE|username
        self.sock.sendall(encode_message(msg)) # Gửi lên server

    def receive_loop(self, callback): # Hàm nhận dữ liệu từ server (chạy ở thread riêng)

        def run(): # Hàm chạy trong thread

            buffer = ""
            # Buffer dùng để tích lũy dữ liệu nhận được
            # Vì TCP có thể nhận dữ liệu không trọn vẹn từng message

            while self.running: # Lặp liên tục khi client còn chạy
                try:
                    data = self.sock.recv(1024) # Nhận tối đa 1024 bytes từ server
                    if not data:
                        break # Nếu không còn dữ liệu → server đóng kết nối
                    buffer += data.decode("utf-8") # Decode bytes → string rồi cộng vào buffer

                    while "\n" in buffer:
                        # Vì mỗi message kết thúc bằng "\n"
                        # nên dùng để tách message hoàn chỉnh

                        raw, buffer = buffer.split("\n", 1) # Tách 1 message ra khỏi buffer
                        msg = decode_message(raw) # Parse message thành dict
                        callback(msg) # Gọi hàm xử lý (ở client.py là handle_message)

                except Exception as e:
                    print("Receive error:", e) # In lỗi nếu có vấn đề khi nhận dữ liệu
                    break # Thoát vòng lặp nếu lỗi

        thread = threading.Thread(target=run, daemon=True)
        # Tạo thread mới để chạy hàm run()
        # daemon=True → thread tự tắt khi chương trình chính kết thúc

        thread.start() # Bắt đầu thread (bắt đầu nhận dữ liệu song song)

    def close(self): # Đóng kết nối
        self.running = False # Dừng vòng lặp nhận dữ liệu
        self.sock.close() # Đóng socket TCP

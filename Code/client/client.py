from client.network import NetworkClient
# Import lớp NetworkClient để xử lý kết nối TCP (connect, send, receive)


class ChatClient:
    # Lớp đại diện cho client chat (logic phía người dùng)

    def __init__(self, username):
        # Hàm khởi tạo khi tạo một client mới

        self.username = username
        # Lưu tên người dùng (dùng để gửi lên server)

        self.network = NetworkClient()
        # Tạo đối tượng network để xử lý giao tiếp TCP với server

    def start(self):
        # Hàm bắt đầu chạy client

        self.network.connect()
        # Kết nối tới server (mở socket TCP)

        self.network.send_join(self.username)
        # Gửi message JOIN để thông báo với server rằng user đã tham gia

        self.network.receive_loop(self.handle_message)
        # Bắt đầu một thread riêng để luôn lắng nghe message từ server
        # Khi nhận được message → gọi hàm handle_message()

        self.chat_loop()
        # Bắt đầu vòng lặp nhập tin nhắn từ bàn phím

    def chat_loop(self):
        # Vòng lặp chính để người dùng nhập tin nhắn

        while True:
            # Lặp vô hạn cho đến khi user thoát

            text = input()
            # Nhận input từ bàn phím

            if text == "/quit":
                # Nếu user nhập lệnh thoát

                self.network.send_leave(self.username)
                # Gửi message LEAVE lên server

                self.network.close()
                # Đóng kết nối socket

                break
                # Thoát vòng lặp → kết thúc chương trình

            self.network.send_message(self.username, text)
            # Gửi tin nhắn bình thường lên server

    def handle_message(self, msg):
        # Hàm xử lý message nhận được từ server

        msg_type = msg.get("type")
        # Lấy loại message (JOIN, MSG, LEAVE)

        if msg_type == "JOIN":
            # Nếu có người mới tham gia

            print(f"{msg['username']} joined the chat")
            # In ra màn hình

        elif msg_type == "MSG":
            # Nếu là tin nhắn chat

            print(f"{msg['username']}: {msg['text']}")
            # Hiển thị dạng: username: nội dung

        elif msg_type == "LEAVE":
            # Nếu có người rời khỏi

            print(f"{msg['username']} left the chat")
            # In thông báo

        else:
            # Nếu message không đúng định dạng

            print("Unknown message:", msg)
            # In ra để debug

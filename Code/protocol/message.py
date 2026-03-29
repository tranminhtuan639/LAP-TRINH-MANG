"""
protocol/message.py
-------------------
Module này định nghĩa "ngôn ngữ chung" của toàn bộ hệ thống chat.

Tất cả các thành phần (server, client, GUI) đều dùng chung module này
để xây dựng, mã hóa và giải mã tin nhắn trước khi gửi/nhận qua socket TCP.

QUAN TRỌNG: Module này phải được hoàn thành TRƯỚC KHI bất kỳ ai
bắt đầu viết server/ hay client/.

Cách import trong các file khác:
    from protocol.message import encode_message, decode_message
    from protocol.message import build_join, build_message, build_leave

Định dạng tin nhắn (giao thức):
    JOIN|username\n          --> khi client mới tham gia
    MSG|username|nội_dung\n  --> khi gửi tin nhắn chat
    LEAVE|username\n         --> khi client rời khỏi phòng chat

Ví dụ thực tế:
    "JOIN|Alice\n"
    "MSG|Alice|Xin chào mọi người!\n"
    "LEAVE|Alice\n"
"""

# =============================================================================
# HẰNG SỐ DÙNG CHUNG
# =============================================================================

# Các loại tin nhắn được hỗ trợ
MSG_JOIN  = "JOIN"   # client vừa kết nối và tham gia phòng chat
MSG_MSG   = "MSG"    # tin nhắn chat thông thường
MSG_LEAVE = "LEAVE"  # client rời khỏi phòng chat

# Ký tự kết thúc mỗi tin nhắn khi truyền qua TCP
# Lý do cần \n: TCP là byte stream, không tự phân biệt ranh giới giữa các tin.
# Server/Client dùng \n để biết "đây là điểm kết thúc của 1 tin nhắn hoàn chỉnh".
DELIMITER = "\n"

# Ký tự phân cách các trường bên trong một tin nhắn
# Ví dụ: "MSG|Alice|Hello" --> ['MSG', 'Alice', 'Hello']
SEPARATOR = "|"


# =============================================================================
# CÁC HÀM XÂY DỰNG TIN NHẮN (BUILD)
# Nhận vào thông tin --> trả về chuỗi string theo đúng định dạng giao thức
# Lưu ý: các hàm này chưa mã hóa thành bytes, chỉ tạo ra chuỗi string thuần.
#         Muốn gửi qua socket thì phải gọi thêm encode_message() ở bước sau.
# =============================================================================

def build_join(username: str) -> str:
    """
    Tạo tin nhắn thông báo tham gia phòng chat.

    Tham số:
        username (str): Tên người dùng muốn tham gia.

    Trả về:
        str: Chuỗi tin nhắn theo định dạng "JOIN|username"

    Ví dụ:
        build_join("Alice")  -->  "JOIN|Alice"
        build_join("Bob")    -->  "JOIN|Bob"
    """
    return f"{MSG_JOIN}{SEPARATOR}{username}"


def build_message(username: str, text: str) -> str:
    """
    Tạo tin nhắn chat thông thường.

    Tham số:
        username (str): Tên người gửi tin nhắn.
        text     (str): Nội dung tin nhắn muốn gửi.

    Trả về:
        str: Chuỗi tin nhắn theo định dạng "MSG|username|nội_dung"

    Ví dụ:
        build_message("Alice", "Xin chào!")       -->  "MSG|Alice|Xin chào!"
        build_message("Bob",   "Hello | World")   -->  "MSG|Bob|Hello | World"

    Lưu ý:
        Dùng maxsplit=2 khi split nên nội dung có thể chứa ký tự '|'
        mà không bị tách nhầm. Ví dụ "Hello | World" vẫn là 1 trường text.
    """
    return f"{MSG_MSG}{SEPARATOR}{username}{SEPARATOR}{text}"


def build_leave(username: str) -> str:
    """
    Tạo tin nhắn thông báo rời khỏi phòng chat.

    Tham số:
        username (str): Tên người dùng muốn rời đi.

    Trả về:
        str: Chuỗi tin nhắn theo định dạng "LEAVE|username"

    Ví dụ:
        build_leave("Alice")  -->  "LEAVE|Alice"
    """
    return f"{MSG_LEAVE}{SEPARATOR}{username}"


# =============================================================================
# HÀM MÃ HÓA (ENCODE)
# Chuyển chuỗi string thành bytes để gửi qua socket TCP.
# Đây là bước CUỐI CÙNG trước khi gọi socket.sendall().
# =============================================================================

def encode_message(msg: str) -> bytes:
    """
    Thêm ký tự kết thúc '\n' vào cuối rồi mã hóa thành bytes UTF-8.

    Tại sao cần '\n'?
        TCP là giao thức byte stream -- dữ liệu có thể đến không đủ hoặc
        nhiều tin nhắn bị gộp lại thành một khối. Ký tự '\n' đóng vai trò
        dấu hiệu kết thúc, giúp bên nhận biết "tin nhắn này đã hoàn chỉnh".

    Tại sao dùng UTF-8?
        Để hỗ trợ tiếng Việt và ký tự đặc biệt trong tin nhắn.

    Tham số:
        msg (str): Chuỗi tin nhắn chưa có '\n', ví dụ "MSG|Alice|Xin chào"

    Trả về:
        bytes: Dữ liệu bytes sẵn sàng gửi qua socket.

    Ví dụ:
        encode_message("JOIN|Alice")        -->  b"JOIN|Alice\n"
        encode_message("MSG|Alice|Hello")   -->  b"MSG|Alice|Hello\n"

    Cách dùng trong server/client:
        data = encode_message(build_join("Alice"))
        socket.sendall(data)
    """
    return (msg + DELIMITER).encode("utf-8")


# =============================================================================
# HÀM GIẢI MÃ (DECODE)
# Chuyển chuỗi string thô (đã bỏ '\n') thành dict Python dễ xử lý.
# Đây là bước ĐẦU TIÊN sau khi nhận được dữ liệu từ socket.
# =============================================================================

def decode_message(raw: str) -> dict:
    """
    Phân tích một tin nhắn thô thành dict Python để dễ xử lý.

    Lưu ý quan trọng:
        - Tham số 'raw' phải là chuỗi đã được bỏ '\n' ở cuối (đã strip).
        - Trong thực tế, raw được tách ra từ buffer như sau:
            raw, buffer = buffer.split("\n", 1)
            msg = decode_message(raw.strip())

    Tham số:
        raw (str): Chuỗi tin nhắn thô, ví dụ "MSG|Alice|Xin chào"

    Trả về:
        dict: Tùy theo loại tin nhắn:
            - JOIN  --> {"type": "JOIN",  "username": "Alice"}
            - MSG   --> {"type": "MSG",   "username": "Alice", "text": "Xin chào"}
            - LEAVE --> {"type": "LEAVE", "username": "Alice"}
            - Lỗi   --> {"type": "UNKNOWN", "raw": <chuỗi gốc>}

    Ví dụ:
        decode_message("JOIN|Alice")
            --> {"type": "JOIN", "username": "Alice"}

        decode_message("MSG|Alice|Xin chào mọi người!")
            --> {"type": "MSG", "username": "Alice", "text": "Xin chào mọi người!"}

        decode_message("LEAVE|Bob")
            --> {"type": "LEAVE", "username": "Bob"}

        decode_message("XYZ|abc")
            --> {"type": "UNKNOWN", "raw": "XYZ|abc"}

    Cách dùng trong server/client:
        msg = decode_message(raw)
        if msg["type"] == "MSG":
            print(f'{msg["username"]} nói: {msg["text"]}')
        elif msg["type"] == "JOIN":
            print(f'{msg["username"]} đã tham gia!')
    """
    # Tách chuỗi theo ký tự '|', tối đa 2 lần để phần text không bị tách nhầm
    # Ví dụ: "MSG|Alice|Hello|World" --> ["MSG", "Alice", "Hello|World"]
    parts = raw.split(SEPARATOR, maxsplit=2)

    # Trường hợp chuỗi rỗng hoặc không hợp lệ
    if not parts:
        return {"type": "UNKNOWN", "raw": raw}

    msg_type = parts[0]  # phần tử đầu tiên luôn là loại tin nhắn

    # Trường hợp JOIN: cần ít nhất 2 phần ["JOIN", "username"]
    if msg_type == MSG_JOIN and len(parts) >= 2:
        return {"type": MSG_JOIN, "username": parts[1]}

    # Trường hợp MSG: cần đủ 3 phần ["MSG", "username", "text"]
    elif msg_type == MSG_MSG and len(parts) >= 3:
        return {"type": MSG_MSG, "username": parts[1], "text": parts[2]}

    # Trường hợp LEAVE: cần ít nhất 2 phần ["LEAVE", "username"]
    elif msg_type == MSG_LEAVE and len(parts) >= 2:
        return {"type": MSG_LEAVE, "username": parts[1]}

    # Không khớp với bất kỳ định dạng nào --> trả về UNKNOWN
    # Server/Client nhận UNKNOWN thì bỏ qua, không crash
    return {"type": "UNKNOWN", "raw": raw}

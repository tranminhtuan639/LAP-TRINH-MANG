# UDM_08: Lập trình ứng dụng Chat (GUI) via TCP

Ứng dụng nhắn tin qua giao thức TCP được viết bằng ngôn ngữ Python. Dự án hỗ trợ cả giao diện người dùng (GUI) và giao diện dòng lệnh (CLI).

---

## 📌 Thông tin dự án

- **Mã dự án:** UDM_08
- **Môn học:** Lập trình mạng - 7480201390613
- **Ngôn ngữ lập trình:** Python

---

## 📖 Mô tả

Dự án tập trung xây dựng một ứng dụng chat sử dụng giao thức **TCP/IP** kết hợp với giao diện đồ họa (**GUI**). Người dùng có thể thực hiện gửi và nhận tin nhắn trực tiếp qua giao diện thay vì sử dụng dòng lệnh (CLI).

---

## 📋 Yêu cầu đề tài

- Xây dựng hệ thống Chat Client–Server dựa trên **TCP Socket**.
- Đảm bảo toàn bộ thao tác của người dùng đều thực hiện thông qua giao diện **GUI**.
- Cho phép Client kết nối tới Server để gửi và nhận tin nhắn.

---

## 👥 Thành viên nhóm và nhiệm vụ

| STT | Họ và Tên | MSSV | File đảm nhiệm | Mức độ hoàn thành
|:---:|:---|:---:|:---:|:---:|
| 1 | Trần Minh Tuấn | 082206013432 | protocol/message.py + gui/chat_gui| 100%|
| 2 | Nguyễn Thị Đan Lê | 040306026190 | client/network.py + Word + quay video demo phần 2 |100%|
| 3 | Trần Thị Quỳnh Liên | 036306009850 | client/network.py |100%|
| 4 | Bùi Lê Phước Lộc | 087206000384 | client/client.py |100%|
| 5 | Thái Doãn Mạnh | 040206004894 | server/server.py +quay video demo phần 1| 100%|
| 6 | Lê Văn Quân | 038204032801 | Powerpoint + Hỗ trợ làm word |100%

---

## 📂 Cấu trúc Repository

Dự án được tổ chức theo các thư mục chức năng sau:

- `Code/`: Chứa toàn bộ mã nguồn Python (Server & Client).
- `DOCX/`: Chứa các file báo cáo định dạng Word (.docx).
- `PPTX/`: Chứa file slide thuyết trình (.pptx).
- `Extra/`: Chứa hình ảnh demo và các tài liệu tham khảo bổ sung.

---

## 📂 Cấu trúc thư mục `Code/`

```
Code/
├── client/
│   ├── __init__.py
│   ├── client.py        # Entry point cho giao diện CLI
│   └── network.py       # Xử lý kết nối socket phía client
├── gui/
│   ├── __init__.py
│   └── chat_gui.py      # Xử lý giao diện và luồng nhận tin
├── protocol/
│   ├── __init__.py
│   └── message.py       # Xử lý đóng gói (encode) và giải mã (decode) dữ liệu
├── server/
│   ├── __init__.py
│   └── server.py        # Quản lý các kết nối và broadcast tin nhắn
└── main.py              # Script điều hướng chính (Server/GUI/CLI)
```

---

## 🚀 Hướng dẫn cài đặt và chạy

### 1. Yêu cầu hệ thống

- Python `3.x` đã được cài đặt.
- Thư viện `Tkinter` (thường đi kèm sẵn với Python).

### 2. Khởi động Server

Mở terminal và chạy lệnh sau để mở cổng chờ kết nối (mặc định port `9999`):

```bash
python main.py --server
```

### 3. Khởi động Client (Giao diện đồ họa - GUI)

Đây là chế độ mặc định. Có thể mở nhiều terminal để chạy nhiều client cùng lúc:

```bash
python main.py
```

> Sau khi chạy, một hộp thoại sẽ hiện lên yêu cầu nhập **IP Server** (mặc định `127.0.0.1`), **Port** và **Tên người dùng**.

### 4. Khởi động Client (Giao diện dòng lệnh - CLI)

Nếu muốn chat trực tiếp trong terminal:

```bash
python main.py --cli
```

---

## 🛠 Chức năng chính

| Tính năng | Mô tả |
|:---|:---|
| **Kết nối đa người dùng** | Server sử dụng `threading` để xử lý nhiều kết nối cùng lúc |
| **Lịch sử chat** | Server lưu trữ lịch sử tin nhắn và gửi lại cho thành viên mới khi tham gia |
| **Giao thức tin nhắn** | Sử dụng cấu trúc `LOẠI\|USER\|NỘI_DUNG` kết thúc bằng ký tự xuống dòng (`\n`) |
| **Lệnh đặc biệt** | Gõ `/quit` trong GUI hoặc `quit` trong CLI để thoát an toàn |

---

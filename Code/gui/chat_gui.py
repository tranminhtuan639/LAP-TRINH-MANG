
<<<<<<< HEAD
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client.network import NetworkClient


class ChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TCP Chat")
        self.root.resizable(False, False)

        self.msg_queue = queue.Queue()
        self.client = None
        self.username = ""

        self._build_ui()
        self._ask_connect()
        self.poll_queue()

    def _build_ui(self):
        frame_top = tk.Frame(self.root)
        frame_top.pack(padx=8, pady=(8, 0), fill=tk.BOTH, expand=True)

        self.txt_area = tk.Text(frame_top, state="disabled", height=20, width=55,
                                wrap=tk.WORD, bg="#f5f5f5", relief=tk.FLAT, font=("Arial", 10))
        self.txt_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame_top, command=self.txt_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_area.config(yscrollcommand=scrollbar.set)

        self.txt_area.tag_config("system", foreground="gray", font=("Arial", 9, "italic"), justify="center")
        self.txt_area.tag_config("other", foreground="black", font=("Arial", 10), justify="left", lmargin1=20, lmargin2=20)
        self.txt_area.tag_config("me", foreground="#ff009d", font=("Arial", 10, "bold"), justify="right", rmargin=20)

        frame_bot = tk.Frame(self.root)
        frame_bot.pack(padx=8, pady=8, fill=tk.X)

        self.entry_msg = tk.Entry(frame_bot, font=("Arial", 11))
        self.entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        self.entry_msg.bind("<Return>", lambda e: self.send())

        self.btn_send = tk.Button(frame_bot, text="Gửi", width=8, command=self.send)
        self.btn_send.pack(side=tk.RIGHT, padx=(6, 0))

        self.lbl_status = tk.Label(self.root, text="Chưa kết nối", fg="red", font=("Arial", 9), anchor="w")
        self.lbl_status.pack(fill=tk.X, padx=8, pady=(0, 4))

    def _ask_connect(self):
        host = simpledialog.askstring("Host", "Địa chỉ server:", initialvalue="127.0.0.1", parent=self.root)
        if host is None or not host.strip():
            self.root.destroy(); return

        port_str = simpledialog.askstring("Port", "Cổng:", initialvalue="9999", parent=self.root)
        if port_str is None or not port_str.strip():
            self.root.destroy(); return

        username = simpledialog.askstring("Tên", "Hãy nhập tên của bạn:", parent=self.root)
        if not username or not username.strip():
            self.root.destroy(); return

        self.username = username.strip()
        self.root.title(f"TCP Chat — {self.username}")

        try:
            self.client = NetworkClient(host, int(port_str))
            self.client.connect()
            self.client.send_join(self.username)
            self.client.receive_loop(self.on_received)
            self.lbl_status.config(text=f"Đã kết nối  {host}:{port_str}  ({self.username})", fg="green")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không kết nối được:\n{e}")
            self.root.destroy()

    def on_received(self, msg):
        self.msg_queue.put(msg)

    def poll_queue(self):
        try:
            while True:
                msg = self.msg_queue.get_nowait()
                self._display(msg)
        except queue.Empty:
            pass
        self.root.after(100, self.poll_queue)

    def _display(self, msg):
        self.txt_area.config(state="normal")
        msg_type = msg.get("type")
        if msg_type == "MSG":
            username = msg.get("username", "")
            text = msg.get("text", "")
            tag = "me" if username == self.username else "other"
            self.txt_area.insert(tk.END, f"{username}: {text}\n", tag)
        elif msg_type in ("JOIN", "LEAVE"):
            action = "tham gia" if msg_type == "JOIN" else "đã rời"
            name = msg.get("username", "")
            label = f"{name} (Bạn)" if name == self.username else name
            self.txt_area.insert(tk.END, f"*** {label} {action} đoạn chat ***\n", "system")
        elif msg_type == "system":
            self.txt_area.insert(tk.END, f"  {msg.get('username', '')}\n", "system")
        self.txt_area.config(state="disabled")
        self.txt_area.see(tk.END)

    def send(self):
        text = self.entry_msg.get().strip()
        if not text:
            return
        self.entry_msg.delete(0, tk.END)
        if text.startswith("/"):
            self._handle_command(text)
            return
        if self.client:
            self.client.send_message(self.username, text)

    def _handle_command(self, text):
        cmd = text.split()[0].lower()
        if cmd == "/quit":
            self.on_close()
       ## elif cmd == "/lệnhkhác":   -- thêm lệnh
        else:
            self._display({"type": "system", "username": f"Lệnh không hợp lệ: {cmd}"})

    def on_close(self):
        if self.client:
            try:
                self.client.send_leave(self.username)
            except Exception:
                pass
            self.client.close()
        self.root.destroy()


def run_client():
    root = tk.Tk()
    app = ChatGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
=======
>>>>>>> 3c1f4c1b89ee8554cad2a24f7c743ba0d2683ac0

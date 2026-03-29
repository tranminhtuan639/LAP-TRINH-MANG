import socket 
import threading
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from protocol.message import( decode_message, encode_message, 
                             build_message, build_leave,
                             MSG_JOIN, MSG_MSG, MSG_LEAVE)

class Chatserver:
    def __init__(self, host='0.0.0.0', port= 9999):
        self.host = host 
        self.port = port
        self._clients = {}
        self._lock = threading.Lock()
        self.chat_history: list[str] = []
        self.history_lock = threading.Lock()
        
    def start(self):
            server_sock = socket.socket ( socket.AF_INET, socket. SOCK_STREAM)
            
            # Cho phép restart server nhanh, không bị lỗi
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind((self.host , self.port))
            server_sock.listen()
            print (f"Sever đang chạy {self.host} : {self.port}\n ")
            print ("Chờ xíu ...")

            while True :
                client_sock , address = server_sock.accept()
                print  (f" Có người kết nối từ {address} ")
                client_sock.send("kết nối thành cong \n".encode())
                
                # Tạo thread riêng cho mỗi client, chạy song song
                t = threading.Thread(
                    target= self.handle_client,
                    args= (client_sock, address,),
                    daemon= True  # hàm này tự tắt khi Ctrl+C
                )
                t.start()
            
    def handle_client(self, client_sock: socket.socket, address ):
        buffer = ''
        username = None
        
        try:
            while True:
                data = client_sock.recv(5555)
                if not data:
                    break 
            
                buffer += data.decode('utf-8')
            
                while "\n" in buffer:
                    raw , buffer = buffer.split("\n",1)
                    raw = raw.strip()
                    if not raw :
                        continue
            
                    msg = decode_message(raw)
                    msg_type = msg.get("type")
                
                    if msg_type == MSG_JOIN:
                        username = msg["username"]
                        
                        with self._lock:
                            self._clients[client_sock] = username
                        
                    elif msg_type == MSG_MSG:
                        if username is None:
                            continue  # Chưa JOIN thì bỏ qua tin nhắn
                        text = msg["text"]
                        print(f"[MSG] {username}: {text}")
                        
                            # Broadcast cho tất cả KỂ CẢ người gửi
                            # (để client biết tin đã được server nhận)
                        broadcast(build_message(username, text))

                    elif msg_type == MSG_LEAVE:
                            # Client tự báo rời → thoát vòng lặp
                        break

                    else:
                            # Tin nhắn không hợp lệ → bỏ qua
                        print(f"[WARN] Tin nhắn lạ từ {address}: {raw}")
        except ConnectionResetError:
            print(f"[!] {address} mất kết nối đột ngột")
        except Exception as e:
            print(f"[ERROR] Lỗi với {addr}: {e}")
        finally:
            
        # Dọn dẹp dù thoát theo cách nào
            if username:
                print(f"[LEAVE] {username} ({address})")
                remove_client(client_socket)
                broadcast(build_leave(username))
            else:
                remove_client(client_socket)
            
            
            
            
    
            
            
            
            
        
        

      

           

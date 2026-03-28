import socket 
import threading
from protocol.message import decode_message, encode_message, build_message, build_leave

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
        data = client_sock.recv(5555)
        
        

      

           

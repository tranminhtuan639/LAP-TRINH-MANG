import socket 
import threading

class Chatserver:


    def start(seft):
        sever_sock = socket.socket ( socket.AF_INET, socket. SOCK_STREAM)
        sever_sock.bind(('0.0.0.0',9999))
        sever_sock.listen()
        print ("Sever đang chạy chờ xíu ")

        while True :
            client_sock , address = sever_sock.accept()
            print  (f" Có người kết nối từ {address} ")
            client_sock.send("kết nối thành cong \n".encode())
            client_sock.close()
            print (f"{address} đã ngắt kết nối \n") 
            

            def xu_ly_client(client_sock):
            # nói chuyện với 1 client
                pass

            while True:
                # tạo thread mới cho mỗi client, chạy song song
                t = threading.Thread(target=xu_ly_client, args=(client_sock,))
                
            t.start()



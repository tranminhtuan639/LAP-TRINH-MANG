import socket 
sever_sock = socket.socket ( socket.AF_INET, socket. SOCK_STREAM)
sever_sock.bind(('0.0.0.0',9999))
sever_sock.listen()
print ("Sever đang chạy chờ xíu ")

while True :
    client_sock , address = sever_sock.accept()
    print  (f" Có người kết nối từ {address} ")
    client_sock.send(b"kết nối thành cong6 \n" )
    client_sock.close()
    print (f"{address} đã ngắt kết nối \n")





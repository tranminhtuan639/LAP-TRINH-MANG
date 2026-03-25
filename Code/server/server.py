import socket 
sever_sock = socket.socket ( socket.AF_INET, socket. SOCK_STREAM)
sever_sock.bind(('0.0.0.0',9999))
sever_sock.listen()
print ("Sever đang chạy chờ xíu ")
client_sock , address = sever_sock.accept()





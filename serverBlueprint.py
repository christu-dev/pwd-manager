import threading
import socket

try: 
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[c]: SOCKET CREATED")
except socket.erorr as err:
    print("socket open error")
    exit()

server_binding = ("locahost", 9999)
ss.bind(server_binding)
ss.listen()

def start_connection(c):
        msg = "Welcome to Blueprint!"
        s.send(msg.encode())

    
        response = c.rev(1024).decode()
        print("[S]: Data received from client" + response)

        print("Done")


while True:
     client, addr = ss.accept()
     t2 = threading.Thread(target=start_connection, arg =(client,))
     t2.start

     ss.close()
     exit()

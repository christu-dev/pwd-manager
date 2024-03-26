import threading
import socket


try: 
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[c]: SOCKET CREATED")
except socket.erorr as err:
    print("socket open error")
    exit()

server_binding = ("localhost", 9999)
cs.connect(server)

data_from_server = cs.recv(1024)
message = data_from_server.decode()
print("[C]; the message was" + message)
cs.send(input("Response here: ").encode())
print("Done.")

cs.close()
exit()

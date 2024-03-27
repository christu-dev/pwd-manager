import threading 
#client and server working at the same time
import socket

try:
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[c]: SOCKET CREATED")
except socket.error as err:
    print
    exit() 

   
server_binding = ("localhost", 10000)
cs.connect(server_binding)

#username
data_from_server = cs.recv(1024)

message = data_from_server.decode()

print("[c]: the message was: " + message+"\n")

cs.send(input("Response here: ").encode())

#password
data_from_server = cs.recv(1024)

message = data_from_server.decode()

print("[c]: the message was: " + message+"\n")

cs.send(input("Response here: ").encode())

#password check if correct

data_from_server = cs.recv(1024)

message = data_from_server.decode()

print("[c]: the message was: " + message)

print("Done")
#cs.close()
exit()



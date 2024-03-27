import threading
import socket

try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[c]: SOCKET CREATED")
except socket.error as err:
    print("sock open error")
    exit()

server_binding = ("localhost", 10000)
ss.bind(server_binding)
ss.listen()


username = "" #global username
def check_valid_PWD(s) -> bool:
    return True; 

def start_connection(s):
    msg = "Welcome to Blueprint. Please enter a username"
    s.send(msg.encode()) #server sending the message

    username = s.recv(1024).decode()
    print("[S]: Data recieved from client: " + username)
    #print("Done.")
    take_password(s)

def take_password(s):
    msg = "Please enter your password for " + username
    s.send(msg.encode()) #server sending request for password

    password = s.recv(1024).decode()

    if(check_valid_PWD(password)):
        msg2 = "Password correct, Login success."
        s.send(msg2.encode())
    else:
        msg3 = "Password wrong, Login failed."
        s.send(msg3.encode())



while True:
    client, addr = ss.accept()
    t2 = threading.Thread(target=start_connection, args=(client,))
    t2.start()
   # t2 = threading.Thread(target=take_password, args = (client,) )

    ss.close()
    exit()



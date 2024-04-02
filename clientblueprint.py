# # import threading 
# # import sqlite3
# # # import bcrypt
# # import socket

# # try:
# #     cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #     print("[c]: SOCKET CREATED")
# # except socket.error as err:
# #     print('socket open error: {} \n'.format(err))
# #     exit() 

# # server_binding = ("localhost", 10000)
# # cs.connect(server_binding)

# # #username
# # data_from_server = cs.recv(1024)

# # message = data_from_server.decode()

# # print("[c]: the message was: " + message+"\n")

# # cs.send(input("Response here: ").encode())

# # #password
# # data_from_server = cs.recv(1024)

# # message = data_from_server.decode()

# # print("[c]: the message was: " + message+"\n")

# # cs.send(input("Response here: ").encode())

# # #password check if correct

# # data_from_server = cs.recv(1024)

# # message = data_from_server.decode()

# # print("[c]: the message was: " + message)




# # print("Done")
# # #cs.close()
# # exit()

# import threading
# import socket

# try:
#     cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     print("[c]: SOCKET CREATED")
# except socket.error as err:
#     print('socket open error: {} \n'.format(err))
#     exit()

# server_binding = ("localhost", 10000)
# cs.connect(server_binding)

# # username
# data_from_server = cs.recv(1024)
# message = data_from_server.decode()
# print("[c]: the message was: " + message+"\n")
# cs.send(input("Response here: ").encode())

# # handle sign-up prompt
# data_from_server = cs.recv(1024)
# message = data_from_server.decode()
# print("[c]: the message was: " + message+"\n")

# if "not exist as an account" in message:
#     response = input("Response here: ").encode()
#     cs.send(response)
#     if response.decode().lower() == 'y':
#         # handle new password prompt
#         data_from_server = cs.recv(1024)
#         message = data_from_server.decode()
#         print("[c]: the message was: " + message+"\n")
#         cs.send(input("Response here: ").encode())

# # password
# data_from_server = cs.recv(1024)
# message = data_from_server.decode()
# print("[c]: the message was: " + message+"\n")
# cs.send(input("Response here: ").encode())

# # password check if correct
# data_from_server = cs.recv(1024)
# message = data_from_server.decode()
# print("[c]: the message was: " + message)

# print("Done")
# cs.close()
# exit()

import threading
import socket

try:
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[c]: SOCKET CREATED")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()

server_binding = ("localhost", 10000)
cs.connect(server_binding)

# username
data_from_server = cs.recv(1024)
message = data_from_server.decode()
print("[c]: the message was: " + message+"\n")
cs.send(input("Response here: ").encode())

# handle sign-up or password prompt
data_from_server = cs.recv(1024)
message = data_from_server.decode()
print("[c]: the message was: " + message+"\n")

if "not exist as an account" in message:
    response = input("Response here: ").encode()
    cs.send(response)
    if response.decode().lower() == 'y':
        # handle new password prompt
        data_from_server = cs.recv(1024)
        message = data_from_server.decode()
        print("[c]: the message was: " + message+"\n")
        cs.send(input("Response here: ").encode())
else:
    # handle password prompt
    password_attempts = 0
    while password_attempts < 4: # 3 attempts
        cs.send(input("Response here: ").encode())
        data_from_server = cs.recv(1024)
        message = data_from_server.decode()
        print("[c]: the message was: " + message)
        if "Password correct" in message:
            break
        elif "Try Again" in message:
            password_attempts += 1
        else:
            print("Unexpected message from server: " + message)
            break

print("Done")
cs.close()
exit()

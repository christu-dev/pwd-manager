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
print(message+"\n")
cs.send(input("Response here: ").encode())

# handle sign-up or password prompt
data_from_server = cs.recv(1024)
message = data_from_server.decode()
print(message+"\n")

if "not exist as an account" in message:

    responded = False
    want_to_signUp = False
    while responded == False:

        response = input("Response here: ").encode()
        cs.send(response)

        if response.decode().lower() == 'y':
            # corresponds with Please enter a password in server
            data_from_server = cs.recv(1024)
            message = data_from_server.decode()
            print(message+"\n")
            cs.send(input("Response here: ").encode())
            
            # handle account creation success message
            data_from_server = cs.recv(1024)
            message = data_from_server.decode()
            print(message+"\n") #the client closes after creation success or fail
            responded = True
        elif response.decode().lower() == 'n':
            #corresponds to Thanks for visiting
            data_from_server = cs.recv(1024)
            message = data_from_server.decode()
            print(message+"\n")
            #corresponds to Now closing
            data_from_server = cs.recv(1024)
            message = data_from_server.decode()
            print(message+"\n")
            responded = True
        else:
            data_from_server = cs.recv(1024)
            message = data_from_server.decode()
            print(message+"\n")
            
        
         
else: 
    # handle password prompt
    password_attempts = 0
    while password_attempts < 3:
        print("reached while loop in password prompt")
       # data_from_server = cs.recv(1024)
       # message = data_from_server.decode()
       # print(message+"\n")

        # send password
        response = input("Response here: ").encode()
        cs.send(response)
        
        #corresponds to password correct or password wrong
        data_from_server = cs.recv(1024)
        message = data_from_server.decode()
        print(message+"\n")
        
        if "Password correct" in message:
            break
        elif "Try Again" in message:
            password_attempts += 1
        else:
            print("Unexpected message from server111: " + message)
            break

    data_from_server = cs.recv(1024)
    message = data_from_server.decode()
    print(message+"\n")

print("Done")
cs.close()
exit()



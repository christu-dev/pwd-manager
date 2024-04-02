import threading
import socket
import sqlite3

# Set up database connection with check_same_thread=False to allow access from multiple threads
conn = sqlite3.connect('test.sql', check_same_thread=False)
cursor = conn.cursor()

# Create table for storing user credentials
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
''')
conn.commit()


# Create an account
# Returns True if user was saved successfully, False if username already exists
def save_user(username, password):
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        return False  # Return False if username already exists
    return True  # Return True if user was saved successfully

# Check 
def check_password(username, password):
    cursor.execute('SELECT password FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    if user:
        stored_password = user[0]
        return password == stored_password
    return False  # Return False if user does not exist


# Returns True if Username exists, False if account is not in table.
def check_user_exist(username):
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
        usernameCount = cursor.fetchone()

        if usernameCount == 1:
            return True
        else:
            return False
       
# Server socket setup
try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("\n[S]: SOCKET CREATED")
    server_binding = ("localhost", 10000)
    ss.bind(server_binding)
    ss.listen()

    def start_connection(client_socket):
        try:
            msg = "\nLogin or Sign-up to Blueprint. Please enter a username:"
            client_socket.send(msg.encode())

            username = client_socket.recv(1024).decode()
            print(f"\n[S]: Data received from client: {username}")

            #IF USERNAME EXISTS
            if check_user_exist(username):


                #while loop for passwords
                passwordAttempts = 0
                successBool = False
                while passwordAttempts < 3:
                    msg = "\nPlease enter your password for " + username
                    client_socket.send(msg.encode())
                    password = client_socket.recv(1024).decode()

                    if check_password(username, password):
                        msg2 = "\nPassword correct, Login success."
                        successBool = True
                        passwordAttempts = 3
                    else:
                        msg2 = "\nPassword wrong, Login failed. Try Again"
                        passwordAttempts += 1
                    client_socket.send(msg2.encode())

                if not successBool:
                    msg3 = "\nThree attempts reached. Blueprint Login is now closing..." 
                elif successBool:
                    msg3 = "\nWelcome to Blueprint. You are now logged in."
                else:
                    msg3 = "\nUnknown Error."

                client_socket.send(msg3.encode())
            else: #start of Create an Account pathing

                responded = False
                want_to_signUp = False
                #loop to make sure the client responds with Y or N
                while responded == False:
                    msg = "\n"+username + " does not exist as an account. Would you like to sign up? (Y/N)"
                    msg2 = ""

                    client_socket.send(msg.encode())
                    response = client_socket.recv(1024).decode()

                    if response == 'Y' or response == 'y':
                        want_to_signUp = True
                        responded = True
                    elif response == 'N' or response == 'n':
                        msg2 = "\nThanks for visiting the Blueprint Login Screen."
                        responded = True
                    else:
                        msg2 = "\nIncorrect input. Do Y/N!"
                    
                    client_socket.send(msg2.encode())
               

                if want_to_signUp:
                    msg3 = "\nPlease enter a password for new user " + "'" + username + "'"
                    client_socket.send(msg3.encode())
                    newpassword = client_socket.recv(1024).decode()
                    
                    
                    if save_user(username, newpassword): #below here ////////////////
                        # msg4 = "\nNew account created with the following info: \nUsername: " +username+" \nPassword: "+password+"\nPlease save this info as there is no way to recover your account once your password is lost!"
                        msg4 = "\nNew account created with the following info: \nUsername: " + username + " \nPassword: " + newpassword + "\nPlease save this info as there is no way to recover your account once your password is lost!"
                    else: #say someone signs up right as you are signing up. Because of concurrent processes, this failure is an option.
                        msg4 = "\nFailed to create account, username exists already! Please try again from the start."
                    client_socket.send(msg4.encode())
                else:
                    msg3 = "\nNow closing..."
                    client_socket.send(msg3.encode())
        finally:
            client_socket.close()

    while True:
        client_socket, addr = ss.accept()
        print(f"[S]: Connection established with {addr}")
        threading.Thread(target=start_connection, args=(client_socket,)).start()
except KeyboardInterrupt:
    print("[S]: Server is shutting down.")
except Exception as e:
    print(f"[S]: An error occurred: {e}")

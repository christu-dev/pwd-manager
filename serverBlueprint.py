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

def save_user(username, password):
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        return False  # Return False if username already exists
    return True  # Return True if user was saved successfully

def check_password(username, password):
    cursor.execute('SELECT password FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    if user:
        stored_password = user[0]
        return password == stored_password
    return False  # Return False if user does not exist

# Server socket setup
try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[S]: SOCKET CREATED")
    server_binding = ("localhost", 10000)
    ss.bind(server_binding)
    ss.listen()

    def start_connection(client_socket):
        try:
            msg = "Welcome to Blueprint. Please enter a username"
            client_socket.send(msg.encode())

            username = client_socket.recv(1024).decode()
            print(f"[S]: Data received from client: {username}")

            msg = "Please enter your password for " + username
            client_socket.send(msg.encode())

            password = client_socket.recv(1024).decode()

            # Try to save the user, or check the password if user already exists
            if not save_user(username, password):
                if check_password(username, password):
                    msg2 = "\nPassword correct, Login success."
                else:
                    msg2 = "\nPassword wrong, Login failed."
                client_socket.send(msg2.encode())

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

finally:
    ss.close()  # Close the server socket
    conn.close()  # Close the database connection when server shuts down
    print("[S]: Server is closed.")


# Import socket module
import socket
# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 52222

# connect to the server on local computer
s.connect(('127.0.0.1', port))

#method to send string to server
def send_string_client(string):
    s.send(string.encode())

#method to recieve string from server
def receive_string_client():
    # (NEED TO TEST IF RECV SIZE OF 1024 IS SUFICIENT FOR ALL STRING SIZES WE WILL USE)
    data = s.recv(1024).decode()  # receive response and decode
    print('Received from server: ' + data)  # display recieved message

receive_string_client()

# close the connection

s.close()

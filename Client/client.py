import socket
import threading
import sys
from unittest import runner


def setup():
    s = socket.socket()             # Create a socket object
    port = 52222                    # Define the port on which you want to connect
    s.connect(('127.0.0.1', port))  # Connect to the server
    return s

s = setup()
 
# Define the port on which you want to connect
port = 52222


#method to send string to server
def send_string_to_server(message):
    s.send(message.encode())

#method to recieve string from server
def receive_data():
    # (NEED TO TEST IF RECV SIZE OF 1024 IS SUFICIENT FOR ALL STRING SIZES WE WILL USE)
    # print('Inside of receive_data')
    # print(s)
    data = s.recv(1024).decode()  # receive response and decode
    # print('data')
    # print(f'data: {data}')  # display recieved message
    return data
def check_if_response_req(data):
    # print('made it to the check_if_response_req function')
    # print(data)
    res_req = False
    last_char = data[len(data) - 1]
    # print(f'last char: {last_char}')
    if last_char == "\u2404":
        # print(f'Data before slice: {data}')
        data = data[:-1]
        # print(f'Data after slice: {data}')
        res_req = True
    print(f'{data}')
    return res_req

running = True
while running:
    # print('entered while loop')
    received_data = receive_data()
    # print(f'received data: {received_data}')
    if check_if_response_req(received_data):
        # print('activated if statement')
        user_input = input("->")
        send_string_to_server(user_input)
    else:
        # print('about to send empty string')
        send_string_to_server('') 
    # if received_string == "kill":
    #     breaks

"""
while True:
    recvStr = recieve_string_from_server()
    if recvStr == "1":
         message = input("->")
         send_string_to_server(message)
    elif recvStr == "kill"
        break

"""
# close the connection
print("Client is shutdown")
s.close()

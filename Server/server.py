# first of all import the socket library
import socket   
import re         
# from DefProgProject.user import *
from user import *
from helper_functions import *


def create_user():
  entered_username = input('Please enter a username.')
  seeking_username = True
  while seeking_username:
    if not re.match("[A-Za-z0-9]+", entered_username):
      print("Only alphanumerics are allowed.")
    elif len(entered_username) < 3 or len(entered_username) > 12:
      print('Usernames must be between 3 and 12 characters.')
    else:
      seeking_username = False
  seeking_password = True
  while seeking_password:
    entered_password = input('Please enter a password.')
    # if re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", entered_password):
    #   seeking_password = False
    # else:
    #   print('Please enter a valid password.')
    seeking_password = False #Just for testing purposes
  print('about to add to user_info')
  input_new_user(entered_username, entered_password)

def server_setup():
  # next create a socket object
  s = socket.socket()
  print("Socket successfully created")

  # reserve a port on your computer in our
  # case it is 12345 but it can be anything
  port = 52222

  # Next bind to the port
  # we have not typed any ip in the ip field
  # instead we have inputted an empty string
  # this makes the server listen to requests
  # coming from other computers on the network
  s.bind(('', port))
  print("socket binded to %s" % (port))

  # put the socket into listening mode
  s.listen(5)
  print("socket is listening")

  # Establish connection with client.
  c, addr = s.accept()
  print('Got connection from', addr)

  #return the client
  return c

def create_user_test():
  entered_username = input('Please enter a username.')
  seeking_username = True
  while seeking_username:
    if not re.match("[A-Za-z0-9]+", entered_username):
      print("Only alphanumerics are allowed.")
    elif len(entered_username) < 3 or len(entered_username) > 12:
      print('Usernames must be between 3 and 12 characters.')
    else:
      seeking_username = False
  seeking_password = True
  while seeking_password:
    entered_password = input('Please enter a password.')
    # if re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", entered_password):
    #   seeking_password = False
    # else:
    #   print('Please enter a valid password.')
    seeking_password = False #Just for testing purposes
  print('about to add to user_info')
  input_new_user(entered_username, entered_password)

def input_new_user(username, password):
  f = open("server/users.txt", "a")
  #defaults ticket count to 0 and leaves events blank
  f.write(f'{username},{password},0,\n') #<- swapped colon to comma
  f.close()

def validate_credentials(username, password):
  validated = False
  user_line = parse_user(username)
  if user_line:
    delimiter_indices = find_delimiters(user_line)
    stored_password = user_line[delimiter_indices[0] + 1:delimiter_indices[1]]
    print('stored password: ' + stored_password)
    print('entered password: ' + password)
    if password == stored_password:
      print('User validated')
      validated = True
    else:
      print('User failed to validate')
  return validated

def load_user():
  entered_username = input('Please enter a username.')
  entered_password = input('Please enter a password.')
  print('About to execute if')
  if validate_credentials(entered_username, entered_password):
    print('about to instantiate user')
    current_user = User(entered_username)
    print('about to execute toString()')
    current_user.__str__()
  # asks the user for username/password
  # if validated, creates a new user object from the entered information

def display_events():
  with open('server/events.txt') as f:
    contents = f.read()
    print(contents)
    f.close()

#method to send a string to specified client
def send_string_server(client, string):
  client.send(string.encode()) # Encode and send to client


# method to receive string from specified client
def receive_string_server(client):
  # (NEED TO TEST IF RECV SIZE OF 1024 IS SUFICIENT FOR ALL STRING SIZES WE WILL USE)
  data = client.recv(1024).decode()  # receive response and decode
  print('Received from client: ' + data)  # display received message


def main():
  client = server_setup()
  main_menu = "\n1.View Events\n2.Purchase Tickets\n3.View Points\n4.Add Points\n5.Exit"
  send_string_server(client, main_menu)


main()

# validate_credentials()
# create_user()
#load_user()
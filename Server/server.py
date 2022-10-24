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

def load_user(entered_username, entered_password):
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
def send_string_to_client(client, message):
  client.send(message.encode()) # Encode and send to client


# method to receive string from specified client
def receive_string_from_client(client):
  # (NEED TO TEST IF RECV SIZE OF 1024 IS SUFICIENT FOR ALL STRING SIZES WE WILL USE)
  data = client.recv(1024).decode()  # receive response and decode
  print('Received from client: ' + data)  # display received message
  return data

def make_client_disconnect(client):
  send_string_to_client(client, "kill")

#Testing client interaction, specifically the first login menu
def client_server_interaction_test():
  client = server_setup()
  main_menu = "\n1.View Events\n2.Purchase Tickets\n3.View Points\n4.Add Points\n5.Exit"
  login_menu = "\n1.Sign-Up\n2.Log-In\n5.Exit"

  while True:
    send_string_to_client(client, login_menu)
    client_input = receive_string_from_client(client)

    #Client creating a new User
    if client_input == "1":
      send_string_to_client(client, "Enter a username")
      client_username = receive_string_from_client(client)
      send_string_to_client(client, "Enter a password")
      client_password = receive_string_from_client(client)
      input_new_user(client_username,client_password)
      #You would load the user here
      break

    #Client logging in as existing user
    elif client_input == "2":
      send_string_to_client(client, "Enter a username")
      client_username = receive_string_from_client(client)
      send_string_to_client(client, "Enter a password")
      client_password = receive_string_from_client(client)

      #Check if user successfully validates
      if validate_credentials(client_username, client_password):
        load_user(client_username, client_password)
        send_string_to_client(client, "LOGGED IN, press ENTER to continue")
        #exit loop if valid just for testing


      #POTENTIAL BUG WE CAN PUT IN OUR CODE, WHEN PROMTED WITH THIS AS CLENT; INPUT A VALUE INSTEAD OF JUST PRESSING ENTER
      send_string_to_client(client, "Invalid username or password, press ENTER to continue")

    #if client desides to exit, close connection
    elif client_input == "5":
      make_client_disconnect(client)


  print("Server is shutdown")

client_server_interaction_test()

# validate_credentials()
# create_user()
#load_user()
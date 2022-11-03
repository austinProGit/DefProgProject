# first of all import the socket library
from pydoc import cli
import socket
import re         
# from DefProgProject.user import *
from user import *
from helper_functions import *
import os
import sys
from event import *

def server_setup():
  s = socket.socket()
  print("Socket successfully created")
  port = 52222
  s.bind(('', port))
  s.listen(5)
  c, addr = s.accept()
  return s, c

def create_new_user(client):
  send_string_expect_response(client, "Enter a username.")
  entered_username = receive_string_from_client(client)
  seeking_username = True
  while seeking_username:
    if not re.match("[A-Za-z0-9]+", entered_username):
      send_string_to_client(client,"Only alphanumerics are allowed.")
    elif len(entered_username) < 3 or len(entered_username) > 12:
      print('Usernames must be between 3 and 12 characters.')
    else:
      seeking_username = False
  seeking_password = True
  while seeking_password:
    send_string_expect_response(client, "Enter a password.")
    entered_password = receive_string_from_client(client)
    # if re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", entered_password):
    #   seeking_password = False
    # else:
    #   print('Please enter a valid password.')
    seeking_password = False #Just for testing purposes
  f = open("server/users.txt", "a")
  #defaults ticket count to 0 and leaves events blank
  f.write(f'{entered_username},{entered_password},0,\n') #<- swapped colon to comma
  f.close()
  current_user = User(entered_username)
  print(f'User {str(current_user.username)} has been loaded.')
  send_string_to_client(client, f'User {str(current_user.username)} has been loaded.')
  return current_user

def validate_credentials(username, password):
  print('Executing validate_credentials')
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

def load_user(client):
  print('Executing load_user')
  current_user = None
  # print('About to validate user')
  send_string_expect_response(client, "Enter a username")
  entered_username = receive_string_from_client(client)
  send_string_expect_response(client, "Enter a password")
  entered_password = receive_string_from_client(client)
  if validate_credentials(entered_username, entered_password):
    # print('about to instantiate user')
    current_user = User(entered_username)
    print('User is loaded')
    print(f'current user: {current_user}')
    # print('about to execute toString()')
    # current_user.__str__()
  else:
    print('Unable to load user.')
  return current_user

def display_user_information(client, user):
  send_string_to_client(client, str(user))

def add_points(client, user):
  send_string_expect_response(client, 'Please enter the number of points to add.')
  points_to_add = int(receive_string_from_client(client))
  user.add_points(points_to_add)
  send_string_to_client(client, f'You have added {points_to_add} points and now have {user.points} points.')
  print(f'You have added {points_to_add} points and now have {user.points}')

def display_events():
  with open('server/events.txt') as f:
    contents = f.read()
    print(contents)
    f.close()

def purchase_tickets(client, user):
  event_str = ''
  line_count = 0
  send_string_expect_response(client, 'Please enter the event for which you wish to purchase tickets.')
  search_event = str(receive_string_from_client(client))
  with open('server/events.txt') as f:
    lines = f.readlines()
    print(lines)
    print(f'search_event: {search_event}')
    event_found = False
    for line in lines:
      # print(f'line: {line}')
      if line[:4] == 'name' and search_event in line:
        send_string_to_client(client, f'Event {search_event} found.')
        # event_str += lines[line_count : line_count + 3]
        event = Event(lines[line_count].replace("\n", ""), lines[line_count + 1].replace("\n", ""), lines[line_count + 2].replace("\n", ""), lines[line_count + 3].replace("\n", ""))
        # print(f'Event: {event}')
        save_str = event.save_str()
        print(f'Save string: {save_str}')
        user.add_event(save_str)
        event_str = event_str + lines[line_count] + lines[line_count + 1] + lines[line_count + 2] + lines[line_count + 3] 
        print(f'Event string: {event_str}')
        user.display_events()
        event_found = True
        break
      line_count += 1
    if not event_found:
      send_string_to_client(client, f'Event {search_event} not found')
    

#method to send a string to specified client
def send_string_to_client(client, message):
  print(f'Sending this string to client: {message}. No response expected')
  client.send(message.encode()) # Encode and send to client

#method to send string to specified client with response character on end of message
def send_string_expect_response(client, message):
  # client.send(message+u"\u0003".encode())
  print(f'Sending this string to client: {message}. Response expected')
  client.send((message+"\u2404").encode())

# method to receive string from specified client
def receive_string_from_client(client):
  # (NEED TO TEST IF RECV SIZE OF 1024 IS SUFICIENT FOR ALL STRING SIZES WE WILL USE)
  data = client.recv(1024).decode()  # receive response and decode
  print('Received from client: ' + data)  # display received message
  return data

def make_client_disconnect(client, socket):
  send_string_to_client(client, "Byebye")
  socket.close()
  sys.exit()

#Testing client interaction, specifically the first login menu
def client_server_login_menu(socket, client):
  print('Executing client_server_login_menu')
  #this was for testing
  login_menu = "\n1.Sign-Up\n2.Log-In\n5.Exit"

  continue_displaying_menu = True
  while continue_displaying_menu:
    send_string_expect_response(client, login_menu)
    client_input = receive_string_from_client(client)

    #Client creating a new User
    if client_input == "1":
      user = create_new_user(client)
      continue_displaying_menu = False

    #Client logging in as existing user
    elif client_input == "2":
      user = load_user(client)
      if user:
        send_string_to_client(client, "LOGGED IN")
        continue_displaying_menu = False
        #exit loop if valid just for testing
      else:
        # POTENTIAL BUG WE CAN PUT IN OUR CODE, WHEN PROMTED WITH THIS AS CLENT; INPUT A VALUE INSTEAD OF JUST PRESSING ENTER
        send_string_to_client(client, "Invalid username or password")
    #if client desides to exit, close connection
    elif client_input == "5":
      continue_displaying_menu = False
      make_client_disconnect(client, socket)
  print('Reached the return statement on login menu.')
  return user

def shutdown(client, socket, user):
  # open user file, find the line where the user's old info is
  # overwrite that old line, close user file
  # break server connection
  print('executing the shutdown function')
  try:
    with open('server/users.txt') as f:
      print('successfully got past the as f line')
      with open('server/users.tmp.txt', 'w') as ft:
        print('successfully got past the as ft line')
        lines = f.readlines()
        print(lines)
        for line in lines:
          if line.find(user.username) == -1:
            ft.write(line)
          else:
            print('Found the user info')
            print(line)
        ft.write(user.save_str())
      ft.close()
    f.close()
    os.remove('server/users.txt')
    os.rename('server/users.tmp.txt', 'server/users.txt')
  except Exception as err:
    print(f'Error: {err}')
  make_client_disconnect(client, socket)


def client_server_main_menu(socket, client, user):
  main_menu = "\n1.Display User Information\n2.Add Points\n3.Purchase Tickets\n4.Cancel Event\n5.Exit"
  continue_displaying_menu = True
  while continue_displaying_menu:
    send_string_expect_response(client, main_menu)
    client_input = receive_string_from_client(client)
    # Display User Information
    if client_input == "1":
      display_user_information(client, user)
    # Add points
    elif client_input == "2":
      add_points(client, user)
    # Purchase tickets
    elif client_input == "3":
      purchase_tickets(client, user)
    # Shutdown
    elif client_input == "5":
      print('Shutting down...')
      send_string_to_client(client, 'Shutting down...')
      shutdown(client, socket, user)

def main():
  socket, client = server_setup()
  user = client_server_login_menu(socket, client)
  client_server_main_menu(socket, client, user)

main()
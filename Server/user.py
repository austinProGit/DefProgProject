from helper_functions import *

class User:
    def __init__(self, username):
        user_line = parse_user(username)
        delimiters = find_delimiters(user_line)
        self.username = username
        self.points = int(user_line[delimiters[1] + 1:delimiters[2]])
        self.events = user_line[delimiters[2] + 1:user_line.find('\n')]

    # def __init__(self, username, points = None, events = None):
    #     if points:
    #         self.points = user_line[delimiters[1]:delimiters[2]]
    #     self.username = username
    #     self.points = points
    #     self.events = events

    def display_points(self):
        print(self.points)

    def add_points(self, points_to_add):
        self.points += points_to_add

    def __str__(self):
        return f'Username: {self.username}, Points: {self.points}, Events: {self.events}\n'

# def parse_user(username):
#   user_line = ''
#   with open('server/users.txt') as f:
#     lines = f.readlines()
#     for line in lines:
#       if line.find(username) != -1:
#         print(username, ' exists as a user')
#         user_line = line
#   return user_line

# def find_delimiters(user_line):
#     return [i for i, letter in enumerate(user_line) if letter == ',']
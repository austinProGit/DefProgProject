from helper_functions import *

class User:
    def __init__(self, username):
        user_line = parse_user(username)
        delimiters = find_delimiters(user_line)
        self.username = username
        self.points = int(user_line[delimiters[1] + 1:delimiters[2]])
        self.events = user_line[delimiters[2] + 1:user_line.find('\n')]
        self.password = (user_line[delimiters[0] + 1:delimiters[1]])

    def display_points(self):
        print(self.points)

    def add_points(self, points_to_add):
        self.points += points_to_add

    def add_event(self, event_to_add):
        self.events += event_to_add

    def display_events(self):
        print(f'Now displaying user events: {self.events}')
    
    def save_str(self):
        return f'{self.username},{self.password},{self.points},{self.events}\n'

    def __str__(self):
        return f'Username: {self.username}, Points: {self.points}, Events: {self.events}\n'
def parse_user(username):
  user_line = ''
  with open('server/users.txt') as f:
    lines = f.readlines()
    for line in lines:
      if line.find(username) != -1:
        print(username, ' exists as a user')
        user_line = line
  return user_line

def find_delimiters(user_line):
    return [i for i, letter in enumerate(user_line) if letter == ',']


class Event:
    def __init__(self, name, date, location, price):
        self.name = name
        self.date = date
        self.location = location
        self.price = price

    def save_str(self):
        return f'{self.name},{self.date},{self.location},{self.price}:'

    def __str__(self):
        return f'Event name: {self.name}.\nEvent date: {self.date}\nEvent location: {self.location}\nEvent price: {self.price}\n'
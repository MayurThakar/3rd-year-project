class Credentials:
    def __init__(self, ID, NAME):
        self.BASE_URL = 'https://docs.google.com/spreadsheets/d/'
        self.SPREADSHEET_URL = f'{self.BASE_URL}{ID}/gviz/tq?tqx=out:csv&sheet={NAME}'

class Handler():

    def __init__(self):
        pass

    def handle_index(self):
        b = None
        with open('index.html', 'r') as f:
            b = f.read()
        print(b)
        return b
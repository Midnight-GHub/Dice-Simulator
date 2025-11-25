import json

class jsonHandler:
    def __init__(self, path):
        self.path = path

    def load(self):
        with open(self.path, 'r') as file:
            return json.load(file)

    def dump(self, data):
        with open(self.path, 'w') as file:
            json.dump(data, file, indent=4)
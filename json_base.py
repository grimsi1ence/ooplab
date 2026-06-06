import json
class JsonOperations:
    def __init__(self, filename: str):
        self.filename=filename
    def save_to_json(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)
    def read_json(self):
        with open(self.filename, 'r') as f:
            read_data=json.load(f)
            return read_data
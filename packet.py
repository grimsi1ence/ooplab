import random
class Packet:
    def __init__(self, src, dest, payload, size, protocol):
        self.src = src
        self.dest = dest
        self.size = size
        self.payload=payload
        self.protocol = protocol
        self.visited = []
    def return_packet(self):
        if random.random()<0.15:
            return None
        return f'{self.src}-{self.dest}-{self.payload}-{self.size}'
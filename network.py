import random
import time
from packet import Packet
class Network:
    def __init__(self):
        self.nodes = []
        self.loss_rate = random.uniform(0.10, 0.15)
        self.packets_sent = 0
        self.packets_lost = 0
        self.total_time = 0

    async def simulate(self, protocol, packets=10):
        
        for i in range(packets):
            src, dest = random.sample(self.nodes, 2)
            packet = Packet(src.name, dest.name, "payload", 32, protocol.NAME)
            start = time.time()
            result = await protocol.transmit(packet)
            self.total_time += time.time() - start
            self.packets_sent += 1
            if "lost" in result:
                self.packets_lost += 1
            print(f"Packet {i}: {result}")

    def analyze(self):
        
        avg_time = self.total_time / self.packets_sent
        loss = (self.packets_lost / self.packets_sent) * 100
        bandwidth = (self.packets_sent - self.packets_lost) / self.total_time
        print("Perfomance metrix")
        print(f"Середній час передачі: {avg_time:.4f} с")
        print(f"Втрати пакетів: {loss:.2f}%")
        print(f"Пропускна здатність: {bandwidth:.2f} пак/с")
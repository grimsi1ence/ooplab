import random
from packet import Packet
import asyncio
#5
class TCPProtocol: 
    NAME = "TCP" 
    @staticmethod 
    async def transmit(packet: Packet): 
        while True: 
            await asyncio.sleep(random.uniform(0.05, 0.3)) # затримка 
            data = packet.return_packet() 
            if data is not None: 
                return f"{data} delivered" 
            print("resend") 
class UDPProtocol: 
    NAME = "UDP" 
    @staticmethod 
    async def transmit(packet: Packet):  
        await asyncio.sleep(random.uniform(0.05, 0.3)) # затримка 
        data = packet.return_packet() 
        if data is not None: 
            return f"{data} delivered" 
        return "Packet lost"
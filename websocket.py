import websockets
import asyncio

class Websocket:
    def __init__(self, uri: str):
        self.uri=uri
        self.ws=None
    async def connect(self):
        self.ws= await websockets.connect(self.uri)
        await self.ws.send("qwerty")
        res=await self.ws.recv()
        print(f"відповідь сервера: {res}")
    async def send(self,info):
        await self.ws.send(info)
    async def rx(self):
        res=await self.ws.recv()
        return res
    async def close(self):
        await self.ws.close()
        print("connection lost")
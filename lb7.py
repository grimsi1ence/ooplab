import websockets
import asyncio

uri="wss://ws.postman-echo.com/raw"
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
        print(f"прийнято: {res}")
    async def close(self):
        await self.ws.close()
        print("connection lost")
msg="HL"
async def main():
    websocket = Websocket(uri)
    try:
        await websocket.connect()
        await websocket.send(msg)
        await websocket.rx()
    except Exception as e:
        print(f"error: {e}")
    finally:
        if websocket.ws:
            await websocket.close()
asyncio.run(main())
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync



class MyChaApp(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("Connecting.....")
        await self.accept()


    async def receive(self):
       pass


    async def disconnect(self):
        pass
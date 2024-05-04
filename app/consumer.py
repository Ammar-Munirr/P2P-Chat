import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync



class MyChaApp(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("Connecting.....")
        await self.accept()
        await self.channel_layer.group_add(f"mychat_app{self.scope['user']}",self.channel_name)


    async def receive(self,text_data):
        text_data = json.dumps(text_data)
        await self.channel_layer.group_send(
            f"mycat_app{text_data['user']}",
            {
                'type':'send.msg',
                'msg':text_data['msg']
            }
        )

    async def send_msg(self,event):
        await self.send(event['msg'])

        
    async def disconnect(self):
        pass
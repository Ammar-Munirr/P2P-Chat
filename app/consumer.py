import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
import datetime
from .models import MyChat
from channels.db import database_sync_to_async

User = get_user_model()


class MyChaApp(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("Connecting.....")
        await self.accept()
        await self.channel_layer.group_add(f"mychat_app{self.scope['user']}",self.channel_name)


    async def receive(self,text_data):
        text_data = json.loads(text_data)
        print(text_data)
        await self.channel_layer.group_send(
            f"mychat_app{text_data['user']}",
            {
                'type':'send.msg',
                'msg':text_data['msg']
            }
        )
        await self.save_chat(text_data)


    @database_sync_to_async   
    def save_chat(self,text_data):
        frnd = User.objects.get(username=text_data['user'])
        mychats, created = MyChat.objects.get_or_create(me=self.scope['user'], frnd=frnd)
        # If the object was just created, initialize the 'chats' field as an empty dictionary
        if created:
            mychats.chat = {}
        mychats.chat[str(datetime.datetime.now())+"1"] = {'user': 'me', 'msg': text_data['msg']}
        mychats.save()
        mychats, created = MyChat.objects.get_or_create(me=frnd, frnd=self.scope['user'])
        # If the object was just created, initialize the 'chats' field as an empty dictionary
        if created:
            mychats.chat = {}
        mychats.chat[str(datetime.datetime.now())+"2"] = {'user': frnd.username, 'msg': text_data['msg']}
        mychats.save()

    async def send_msg(self,event):
        await self.send(event['msg'])

    
import datetime
import json

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model

from .models import MyChat

User = get_user_model()


class MyChaApp2(AsyncJsonWebsocketConsumer):
    async def connect(self):
        my_id = self.scope["user"].id
        other_user_id = self.scope["url_route"]["kwargs"]["id"]
        if int(my_id) > int(other_user_id):
            self.room_name = f"{my_id}-{other_user_id}"
        else:
            self.room_name = f"{other_user_id}-{my_id}"

        self.room_group_name = "chat_%s" % self.room_name
        print(self.room_group_name)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def receive(self, text_data):
        text_data = json.loads(text_data)
        print(text_data)
        await self.channel_layer.group_send(self.room_group_name, {"type": "send.msg", "msg": text_data["msg"], "id": text_data["user"]})
        await self.save_chat(text_data)

    @database_sync_to_async
    def save_chat(self, text_data):
        frnd = User.objects.get(id=text_data["user"])
        mychats, created = MyChat.objects.get_or_create(me=self.scope["user"], frnd=frnd)
        if created:
            mychats.chat = {}
        mychats.chat[str(datetime.datetime.now()) + "1"] = {"user": "me", "msg": text_data["msg"]}
        mychats.save()
        mychats, created = MyChat.objects.get_or_create(me=frnd, frnd=self.scope["user"])
        if created:
            mychats.chat = {}
        mychats.chat[str(datetime.datetime.now()) + "2"] = {"user": frnd.id, "msg": text_data["msg"]}
        mychats.save()

    async def send_msg(self, event):
        event = json.dumps({"msg": str(event["msg"]), "id": event["id"]})
        print(event)
        await self.send(event)

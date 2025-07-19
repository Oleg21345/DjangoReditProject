from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
import json
from test_django.chat_models import GroupMessage, ChatGroup
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class ChatroomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        self.chatroom_name = self.scope["url_route"]["kwargs"]["chatroom_name"]
        print(f"[DEBUG] Отримане імʼя кімнати: '{self.chatroom_name}'")

        self.chatroom = await sync_to_async(get_object_or_404)(ChatGroup, group_name=self.chatroom_name)

        await self.channel_layer.group_add(self.chatroom_name, self.channel_name)

        is_user_online = await sync_to_async(self.chatroom.users_online.filter(id=self.user.id).exists)()
        if not is_user_online:
            await sync_to_async(self.chatroom.users_online.add)(self.user)
            await self.update_online_counter()

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.chatroom_name, self.channel_name)

        is_user_online = await sync_to_async(self.chatroom.users_online.filter(id=self.user.id).exists)()
        if is_user_online:
            await sync_to_async(self.chatroom.users_online.remove)(self.user)
            await self.update_online_counter()


    async def receive(self, text_data=None, bytes_data=None):
        print(f"[DEBUG] Received data: {text_data}")
        data = json.loads(text_data)
        body = data.get("body", "").strip()
        if not body:
            return

        message = await sync_to_async(GroupMessage.objects.create)(
            body=body,
            author=self.user,
            chat_group=self.chatroom,
        )

        await self.channel_layer.group_send(
            self.chatroom_name,
            {
                "type": "message_handler",
                "message_id": message.id,
            }
        )

    async def message_handler(self, event):
        message_id = event["message_id"]

        message = await sync_to_async(GroupMessage.objects.get)(id=message_id)

        html = await sync_to_async(render_to_string)(
            "cooking/component/_chat_message.html",
            {"message": message, "user": self.user}
        )

        await self.send(text_data=html)

    async def update_online_counter(self):
        online_count = await sync_to_async(self.chatroom.users_online.count)() - 1

        event = {
            "type": "online_count_handler",
            "online_count": online_count,
        }
        await self.channel_layer.group_send(self.chatroom_name, event)


    async def online_count_handler(self, event):
        online_count = event["online_count"]
        html = await sync_to_async(render_to_string)("cooking/component/_online_counter.html",
                                                     {"online_count": online_count})

        await self.send(text_data=html)







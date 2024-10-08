import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import CustomerChat
from users.models import CustomUser


class PersonalChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("hloooo")
        
        current_user_id = self.scope["url_route"]["kwargs"]["current_user_id"]
        other_user_id = self.scope["url_route"]["kwargs"]["other_user_id"]
        print(current_user_id, other_user_id, "user id got")
        
        if int(current_user_id) > int(other_user_id):
            self.room_name = f"{current_user_id}-{other_user_id}"
        else:
            self.room_name = f"{other_user_id}-{current_user_id}"

        self.room_group_name = "chat_%s" % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, code):
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["message"]
        current_user_id = data["current_user_id"]
        from_user = data["from_user"]
        receiver = data["receiver"]

        await self.save_message(
            user=current_user_id,
            from_user=from_user,
            message=message,
            group_name=self.room_group_name,
            receiver=receiver,
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "current_user_id": current_user_id,
                "from_user": from_user,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        current_user_id = event["current_user_id"]
        from_user = event["from_user"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "current_user_id": current_user_id,
                    "from_user": from_user,
                }
            )
        )

    @database_sync_to_async
    def save_message(self, user, group_name, from_user, message, receiver):
        other_user_id = self.scope["url_route"]["kwargs"]["other_user_id"]

        user = CustomUser.objects.get(pk=user)
        other_user_id = CustomUser.objects.get(pk=other_user_id)

        CustomerChat.objects.create(
            user=user,
            other_user=other_user_id,
            message=message,
            group_name=group_name,
            from_user=from_user,
        )

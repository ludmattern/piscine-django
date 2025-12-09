import json
import hashlib
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message, ConnectedUser
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # Group names must be valid unicode strings containing only ASCII alphanumerics, hyphens, underscores, or periods.
        # We use a hash of the room name to ensure it meets these requirements.
        self.room_group_name = 'chat_%s' % hashlib.md5(self.room_name.encode('utf-8')).hexdigest()

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Send last 3 messages
        await self.send_last_messages()

        # Notify that user has joined
        user = self.scope["user"]
        if user.is_authenticated:
             await self.add_connected_user(user, self.room_name, self.channel_name)
             await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': f'{user.username} has joined the chat',
                    'username': 'System'
                }
            )
             await self.broadcast_user_list()

    async def disconnect(self, code):
        user = self.scope["user"]
        if user.is_authenticated:
            await self.remove_connected_user(self.channel_name)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': f'{user.username} has left the chat',
                    'username': 'System'
                }
            )
            await self.broadcast_user_list()

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"]

        if user.is_authenticated:
            # Save message to database
            await self.save_message(user, self.room_name, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': user.username
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @database_sync_to_async
    def save_message(self, user, room_name, message):
        room = Room.objects.get(name=room_name)
        Message.objects.create(user=user, room=room, content=message)

    async def send_last_messages(self):
        last_messages = await self.get_last_messages(self.room_name)
        for msg in last_messages:
             await self.send(text_data=json.dumps({
                'message': msg['content'],
                'username': msg['username']
            }))

    @database_sync_to_async
    def get_last_messages(self, room_name):
        room = Room.objects.get(name=room_name)
        messages = room.messages.all().order_by('-timestamp')[:3]
        return [{'content': msg.content, 'username': msg.user.username} for msg in reversed(messages)]

    @database_sync_to_async
    def add_connected_user(self, user, room_name, channel_name):
        room = Room.objects.get(name=room_name)
        ConnectedUser.objects.create(user=user, room=room, channel_name=channel_name)

    @database_sync_to_async
    def remove_connected_user(self, channel_name):
        ConnectedUser.objects.filter(channel_name=channel_name).delete()

    @database_sync_to_async
    def get_connected_users(self, room_name):
        room = Room.objects.get(name=room_name)
        return list(room.connected_users.values_list('user__username', flat=True).distinct())

    async def broadcast_user_list(self):
        users = await self.get_connected_users(self.room_name)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_list',
                'users': users
            }
        )

    async def user_list(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': event['users']
        }))

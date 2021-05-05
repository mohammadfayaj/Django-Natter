from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from private_chat.models import PrivateMessage,PrivateRoom
from natter.models import GroupMessage, GroupRoom
from django.contrib.auth.models import User
from natter.middleware import get_request
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
import json


class ChatPrivateConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print(self.room_name)
        self.room_group_name = 'chat_%s' % self.room_name #we need to grabe room_name from model

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        request_username = text_data_json['request_username']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'request_username' : request_username,
            }
        )
        try:
            request_user = self.scope['user']
            get_room = await sync_to_async(PrivateRoom.objects.get, thread_sensitive=True)(room_name=self.room_name)
            results = await database_sync_to_async(PrivateMessage.objects.create, 
                thread_sensitive=True)(msg=message,user=request_user, room=get_room)

            if results is not None:
                final = await database_sync_to_async(PrivateMessage.objects.update, 
                thread_sensitive=True)(parent = results,)
        except:
            get_room = await sync_to_async(GroupRoom.objects.get, thread_sensitive=True)(room_name=self.room_name)
            results = await database_sync_to_async(GroupMessage.objects.create, 
            thread_sensitive=True)(msg=message,user=request_user,room=get_room)

            # if results is not None:
            #     final = await database_sync_to_async(GroupMessage.objects.update, 
            #     thread_sensitive=True)(parent = results,)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        request_username =  event['request_username']

        print(f"this is receive message from room group {message}")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'request_username' : request_username,

        }))





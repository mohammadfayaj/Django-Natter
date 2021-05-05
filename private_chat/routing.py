# chat/routing.py
from django.urls import path

from private_chat import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.ChatPrivateConsumers.as_asgi()),
]
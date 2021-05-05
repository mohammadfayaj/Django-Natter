from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path
from private_chat import views


app_name = 'private_chat'

urlpatterns = [
    path('private_chat/', views.private_chat_view, name='private-chat-home'),
    path('private_chat/<int:id>/', views.private_chat_room_create, name='private-chat-create'),
    path('private_chat/<str:room_name>/', views.unfriend, name='un-friend'),

    path('<str:room_name>/', login_required(views.private_chat_room), name='private-room'),
]

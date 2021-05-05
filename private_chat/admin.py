from django.contrib import admin
from private_chat.models import PrivateRoom, PrivateMessage


admin.site.register(PrivateRoom)
admin.site.register(PrivateMessage)

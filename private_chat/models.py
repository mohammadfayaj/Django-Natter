from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from natter.middleware import get_request
from django.urls import reverse
from django.contrib.auth import get_user
import uuid


class PrivateRoom(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='receiver')
    subscribers = models.ManyToManyField(User, blank=True)
    room_name = models.SlugField(max_length=250, default=uuid.uuid4,)
    is_friend = models.BooleanField(default=False)
    is_unfriend = models.BooleanField(default=False)

    def __str__(self):
        subscribers = self.subscribers.all()
        user = self.sender
        subscribers_list = []
        for i in subscribers:
            subscribers_list.append(i.username)

        if f'{user}' in subscribers_list:
            return " - ".join(subscribers_list)
        else:
            return f"*{user}* - You was unfriend - {subscribers_list}"

    def get_private_friend(self):
        if get_request().user:
            if self.is_friend:
                subscribers = self.subscribers.all()
                subscribers_list = []
                for i in subscribers:
                    if get_request().user != i:
                        subscribers_list.append(i.username)
                return " - ".join(subscribers_list)


class PrivateMessage(MPTTModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,)
    room = models.ForeignKey(PrivateRoom, on_delete=models.SET_NULL, null=True)
    parent = TreeForeignKey('self' , null=True, blank=True, related_name= 'children', db_index=True, on_delete=models.CASCADE)
    msg = models.CharField(max_length= 1000 , null=True,)
    attach_file = models.FileField(upload_to='natter_attach_file', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.msg} sent by "{self.user}" in Room "{self.room}"'

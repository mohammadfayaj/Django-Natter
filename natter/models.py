from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from natter.middleware import get_request
from django.contrib.auth import get_user
from django.urls import reverse
from django.db import models
import uuid

'''
    if sender send a message to an user,  An user should get the message, And if
    he click the message sender id he will inter the same room as sender was created.

    A user can subscribe to many rooms, a room can be linked to many users.
    A message can belong to one user only, but a user may have many messages.
    A room may contain many messages from different users.

'''

# Group Room
class GroupRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='request_user')
    subscribers = models.ManyToManyField(User, blank=True)
    room_name = models.SlugField(max_length=250, default=uuid.uuid4,)
    is_friend = models.BooleanField(default=False)
    is_unfriend = models.BooleanField(default=False)

    def __str__(self):
        subscribers = self.subscribers.all()
        user = self.user
        subscribers_list = []
        # user_list = [user.username]
        for i in subscribers:
            subscribers_list.append(i.username)

        if f'{user}' in subscribers_list:
            return " - ".join(subscribers_list)
        else:
            return f"*{user}* - You was unfriend - {subscribers_list}"
        return self.user


    def get_friend(self):
        subscribers = self.subscribers.all()
        subscribers_list = []
        for i in subscribers:
            if get_request().user != i:
                subscribers_list.append(i.username)

        return " - ".join(subscribers_list)

#Group Message
class GroupMessage(MPTTModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user')
    room = models.ForeignKey(GroupRoom, on_delete=models.SET_NULL, null=True)
    parent = TreeForeignKey('self' , null=True, blank=True, related_name= 'children', db_index=True, on_delete=models.CASCADE)
    msg = models.CharField(max_length= 1000 , null=True,)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    attach_file = models.FileField(upload_to='natter_attach_file', null=True, blank=True)

    def __str__(self):
        return f'{self.msg} sent by "{self.user}" in Room "{self.room}"'


 
    







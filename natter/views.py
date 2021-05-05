from django.core.exceptions import ObjectDoesNotExist
from natter.models import GroupMessage,GroupRoom
from django.shortcuts import render, redirect
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from django.contrib import messages
import collections
import json


def home(request):
    template = 'base/home.html'

    return render(request, template, )


def room(request, room_name):
    template = 'chat/room.html'
    room_name = GroupRoom.objects.get(room_name=room_name)
    group_msg = GroupMessage.objects.filter(room=room_name)

    context = {
        'room_name' : room_name,
        'group_msg' : group_msg,
    }
    return render(request, template, context )

def get_room_name(request):
    try:
        room = GroupRoom.objects.filter(user=request.user)
        for i in room:
            room_name = i.room_name
            get_room = GroupRoom.objects.get(room_name=room_name)
            return get_room.room_name
    except room.DoesNotExist:
        messages.warning(request, 'Group Room Url Not Found!')


# create groop Friend
def create_friend(request, id):
    get_auth_user_id = User.objects.get(id=id)
    request_user_id = request.user.id
    user_id = get_auth_user_id.id

    try:
        get_room = GroupRoom.objects.get(room_name=get_room_name(request),)
        if get_room:
            obj ,update = GroupRoom.objects.update_or_create(user=request.user)
            room_create = obj.subscribers.add(request_user_id, user_id) #subscribers is many to many field
            messages.info(request, 'Group list was updated sucessfully !' )
    except:
        create = GroupRoom.objects.create(user=request.user)
        room_create = create.subscribers.add(request_user_id, user_id)
        messages.info(request, f'Now your are connected with {get_auth_user_id}' )

    return redirect ('natter:index')


def remove_group(request, room_name):
    try:
        room = GroupRoom.objects.get(subscribers=request.user, room_name=room_name)
        room.subscribers.remove(request.user,)
    except:
        pass

    return redirect('natter:index')


def index(request):
    '''
    Get other_user id or Friend
    This query_set will return other_user name
    suppose we have two subscribers  like ['darkwhiser' , 'mohammad']
    darkwhisper friend is mohammad so, mohammad name will appear darkwhiser friend list section
    '''
    user = User.objects.all()
    room_qs = GroupRoom.objects.filter(subscribers=request.user)
    auth_user_list= []
    room_subscribers_list = []
    for u in user:
        auth_user_list.append(u)
    for r in room_qs:
        for i in r.subscribers.all():
            room_subscribers_list.append(i)

    none_friends_list = list(set(auth_user_list) - set(room_subscribers_list)) # remove duplicate him self

    context = {
        "user": user,
        "room_name": room_qs,
        'none_friends_list' : none_friends_list,

    }
    return render(request, 'chat/index.html' , context)


 
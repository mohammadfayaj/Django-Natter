from private_chat.models import PrivateRoom, PrivateMessage
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages


def private_chat_room(request, room_name):
    template = 'private_chat/private_room.html'
    room_name = PrivateRoom.objects.get(room_name=room_name)
    private_msg = PrivateMessage.objects.filter(room=room_name)
    context = {
        'room_name' : room_name,
        'private_msg' : private_msg,
    }   
    return render(request, template, context )

def show_user_without_current_user(request):
    user = User.objects.all()
    auth_user_list = []
    request_user = []
    for i in user:
        auth_user_list.append(i)
    request_user.append(request.user)
    without_current_user = list(set(auth_user_list) - set(request_user))
    
    return without_current_user

def get_none_friend_list(request):
    user = User.objects.all()
    room_qs = PrivateRoom.objects.filter(is_friend=True)
    none_friends_list= None
    for i in room_qs:
        if i.is_friend == True:
            auth_user_list =  []
            room_user_list =  []
            for u in user:
                auth_user_list.append(u)
            for r in room_qs:
                room_user_list.extend([r.receiver, r.sender])
                room_user_list.append(request.user)
            none_friends_list = list(set(auth_user_list) - set(room_user_list)) # remove duplicate him self

            return none_friends_list
        else:
            pass

     
@login_required
def private_chat_view(request):
    user = User.objects.all()
    room_qs = PrivateRoom.objects.filter(subscribers=request.user)

    without_current_user = show_user_without_current_user(request)
    none_friends_list = get_none_friend_list(request)

    context = {
        "user": user,
        "room_name": room_qs,
        'none_friends_list' : none_friends_list,
        'without_current_user': without_current_user,

    }
    return render(request, 'private_chat/private_chat.html' , context)


def get_private_room_name(request):  
    try:
        room = PrivateRoom.objects.filter(is_friend=False)
        for i in room:
            room_name = i.room_name
            return room_name

    except ObjectDoesNotExist:
        messages.warning(request, 'private room url not found!')


@login_required
def private_chat_room_create(request, id):
    get_auth_user_id = User.objects.get(id=id)
    request_user_id = request.user.id
    user_id = get_auth_user_id.id
    try:
        get_room = PrivateRoom.objects.get(
            room_name=get_private_room_name(request),
            is_friend=False,
            )
        get_room.is_friend=True
        get_room.save()
        messages.info(request, f'Now your are Re-connected with {get_auth_user_id}' )

    except:
        room_create = PrivateRoom.objects.create(sender=request.user, receiver=get_auth_user_id, is_friend=True)
        subscribers_add_to_room = room_create.subscribers.add(request_user_id, user_id)
        
        messages.info(request, f'Now your are connected with {get_auth_user_id}' )

    return redirect ('private_chat:private-chat-home')


@login_required
def unfriend(request, room_name):
    try:
        room = PrivateRoom.objects.get(room_name=room_name)
        room.is_friend=False
        room.save()
        messages.info(request, f'Successfully disconnected!' )
    except:
        pass

    return redirect('private_chat:private-chat-home')





from django.shortcuts import render
from django.contrib.auth.models import User
from .models import ChatRoom, ChatData
import uuid
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.http import HttpResponseRedirect
import datetime
# Create your views here.


def login(request):
    return render(request, 'login.html', {})


def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    login_user_id = int(request.user.id)
    all_users = User.objects.all()
    chatrooms = ChatRoom.objects.filter(Q(user_one=request.user) | Q(user_two=request.user))
    users = []
    for i in chatrooms:
        user = {}
        user['name'] = i.user_one.first_name if i.user_one.id != login_user_id else i.user_two.first_name
        user['chatroom_id'] = uuid.UUID(i.chatroom_id)
        user['id'] = i.user_one.id if i.user_one.id != login_user_id else i.user_two.id
        users.append(user)

    for i in all_users:
        if i.id not in [u['id'] for u in users] and i.id != login_user_id:
            user = {}
            user['name'] = i.first_name
            user['chatroom_id'] = None
            user['id'] = i.id
            users.append(user)
    context = {
        'all_users': users,
    }
    return render(request, 'home.html', context)


def chatroom(request, chatroom, remote_user):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    remote_user = User.objects.get(id=int(remote_user))
    user = request.user
    if chatroom:
        chatroom_id = uuid.UUID(chatroom)
        chatroom_obj = ChatRoom.objects.filter(chatroom_id=chatroom_id).order_by('-created_on')[0]
        chats_obj = ChatData.objects.filter(chat_room=chatroom_obj).order_by('created_on')
        chat_data_list = []
        for obj in chats_obj:
            chat_data = {}
            chat_data['user'] = str('me' if obj.user == user else remote_user.first_name + " " + remote_user.last_name)
            chat_data['text'] = obj.chat_text
            chat_data_list.append(chat_data)
        context = {
            'chats': chat_data_list,
            'chatroom_id': chatroom_obj.chatroom_id,
            'remote_user': remote_user,
            'last_message_datetime': chats_obj.reverse()[0].created_on,
        }
    else:
        chatroom_obj = ChatRoom.objects.create(user_one=user, user_two=remote_user)
        context = {
            'chats': [],
            'chatroom_id': chatroom_obj.chatroom_id,
            'remote_user': remote_user,
        }
    return render(request, 'chatroom.html', context)


@require_POST
def update_message(request):
    user = request.user
    message = request.POST.get('message', None)
    chatroom_id = uuid.UUID(request.POST.get('chatroom_id', None))
    if chatroom_id:
        chatroom_obj = ChatRoom.objects.get(chatroom_id=chatroom_id)
        # create chat data
        ChatData.objects.create(user=user, chat_text=message, chat_room=chatroom_obj)
        return JsonResponse({'success': True})


@require_POST
def get_message(request):
    user_1 = request.user
    user_2 = request.POST.get('remote_user', None)
    chatroom_id = uuid.UUID(request.POST.get('chatroom_id', None))
    chatroom_obj = ChatRoom.objects.get(chatroom_id=chatroom_id)
    chats_obj = ChatData.objects.filter(chat_room=chatroom_obj)
    chat_data_list = []
    for obj in chats_obj:
        chat_data = {}
        chat_data['user'] = 'me' if obj.user == user_1 else user_2
        chat_data['text'] = obj.chat_text
        chat_data_list.append(chat_data)
    return JsonResponse({'success': True, 'chat_data_list': chat_data_list})

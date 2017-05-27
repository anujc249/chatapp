from __future__ import unicode_literals
from django.contrib.auth.models import User
from django_extensions.db.fields import UUIDField

from django.db import models

# Create your models here.


class ChatRoom(models.Model):
    chatroom_id = UUIDField(unique=True)
    user_one = models.ForeignKey(User, related_name='user_one')
    user_two = models.ForeignKey(User, related_name='user_two')
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False)


class ChatData(models.Model):
    user = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False)
    chat_text = models.CharField(max_length=1000)
    chat_room = models.ForeignKey(ChatRoom)

from django.contrib import admin
from .models import ChatRoom, ChatData

# Register your models here.


class ChatroomAdmin(admin.ModelAdmin):
    model = ChatRoom


class ChatdataAdmin(admin.ModelAdmin):
    model = ChatData


admin.site.register(ChatRoom, ChatroomAdmin)
admin.site.register(ChatData, ChatdataAdmin)

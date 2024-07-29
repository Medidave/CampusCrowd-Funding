from django.contrib import admin
from .models import Chat_forum, Message, Reply

# Register your models here.
admin.site.register(Chat_forum)
admin.site.register(Message)
admin.site.register(Reply)


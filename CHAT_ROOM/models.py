from django.db import models
from users.models import Project
from users.models import Profile
from django.contrib.auth.models import User
import uuid

import random
import string

def generate_unique_string(length=6):
    letters = string.ascii_lowercase
    unique_string = ''.join(random.choice(letters) for _ in range(length))
    # Ensure uniqueness by checking if the generated unique_string already exists
    while Chat_forum.objects.filter(unique_string=unique_string).exists():
        unique_string = ''.join(random.choice(letters) for _ in range(length))
    return unique_string

# Create your models here.   

class Chat_forum(models.Model):
    host = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, null=True)
    # description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(Profile, related_name='Participants', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    unique_string = models.CharField(max_length=10, unique=True, editable=False, null=True)  
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    class Meta:
        ordering = ['-updated', '-created']

    def save(self, *args, **kwargs):
        if not self.unique_string:
            self.unique_string = generate_unique_string()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.project.project_title
    


class Message(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='Chatter')
    room = models.ForeignKey(Chat_forum, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    image = models.ImageField(max_length=400, null=True, blank=True, upload_to='CampusCrowd/message_images/')
    replies = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    class Meta:
        ordering = ['-updated', '-created']


    def __str__(self):
        return self.body[0:50]


class Reply(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True,)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)
    reply = models.TextField()
    # image = models.ImageField(null=True, blank=True, upload_to='message_images/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    class Meta:
        ordering = ['-updated', '-created']


    def __str__(self):
        return self.reply[0:50]



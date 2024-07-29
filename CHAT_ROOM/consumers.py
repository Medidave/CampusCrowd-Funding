# chat/consumers.py
import json
from django.contrib.auth.models import User

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from . models import Message, Chat_forum, Reply
from users.models import Profile
from django.contrib.auth.models import User
from django.db.models import Q


import os
import base64
import uuid
from django.conf import settings

from botocore.exceptions import ClientError
import boto3

class ChatConsumer(WebsocketConsumer):

    # THIS FUNCTION IS RESPONSOIBLE FOR SAVING DECODING THE IMAGE FROM THE CLIENT SIDE AND SAVING INTO AWS S3 BUCKET
    def save_base64_image_to_s3(self, image_data):

        try:
            # Extract image data and extension
            image_format, data = image_data.split(';base64,')
            extension = image_format.split('/')[-1]  # Extract extension (e.g., png, jpg)

            # Generate a unique filename
            filename = f"{uuid.uuid4()}.{extension}"

            # Create a Boto3 session using credentials from settings
            session = boto3.Session(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                # region_name='eu-north-1'  # THE AWS REGION NAME 
            )

            # Create S3 client with retrieved credentials
            s3_client = session.client('s3')

            # Upload image to S3 bucket
            s3_object_key = f"CampusCrowd/message_images/{filename}"  # Customize object key path if needed
            s3_client.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=s3_object_key,
                Body=base64.b64decode(data),
                ContentType=image_format  # Optionally set content type
            )

            # Return the S3 object URL (modify based on your S3 configuration)
            s3_object_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.eu-north-1.amazonaws.com/{s3_object_key}"

            return s3_object_url

        except (ClientError, Exception) as e:
            print(f"Error saving image to S3: {e}")
            return None  # Or handle error differently (e.g., log, send notification)


    

    def fetch_messages(self, data):
        messages = Message.objects.filter(room__id=data['roomid']).order_by('created')
        
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }

        if (data['command'] == 'send_chat_message'):
            self.send_chat_message(content)
        else:
            self.send_message(content)


    def new_message(self, data):

        author = data['from']
        room = Chat_forum.objects.get(id=data['roomid'])
        author_user = User.objects.get(username=author)
       
        message = Message.objects.create(
            user = author_user.profile,
            room = room,
            body=data['message'],
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    
    def new_image_message(self, data):
        author = data['from']
        message_image = data['image']
        message_image = self.save_base64_image_to_s3(message_image)
        room = Chat_forum.objects.get(id=data['roomid'])
        author_user = User.objects.get(username=author)

        message = Message.objects.create(
            user = author_user.profile,
            room = room,
            image=message_image,
        )

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)


    def process_image_and_text(self, data):
        author = data['from']
        message_image = data['image']
        message_image = self.save_base64_image_to_s3(message_image)
        room = Chat_forum.objects.get(id=data['roomid'])
        author_user = User.objects.get(username=author)
        message = Message.objects.create(
            user = author_user.profile,
            room = room,
            image=message_image,
            body = data['message'],
        )

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)



    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        
        return result


    def return_replies(self, reply):

        return {
                'reply_user_id': str(reply.user.id),
                "reply_user_image": reply.user.profile_image.url,
                'reply_user_firstname': reply.user.user.first_name,
                'body': reply.reply,
                'created': str(reply.created),
                }


    def check_if_message_has_replies(self, message_id):
        try:
          message = Message.objects.get(id=message_id)
        except Message.DoesNotExist:
            return False        
        result = []
        if message.replies:
            for reply in message.reply_set.all().order_by('created'):
                result.append(self.return_replies(reply))
        else:
            result = False
        
        return result

    def message_to_json(self, message):
        return {
            'chatter_username': message.user.user.username,
            'chatter_firstname': message.user.user.first_name,
            'user_image_url': str(message.user.profile_image),
            'user_id': str(message.user.id),
            'message_id': str(message.id),
            'created': str(message.created),
            'message_image_url': str(message.image),
            'message_body': message.body,
            'has_replies': self.check_if_message_has_replies(message.id),
        }

    
    def edit_message(self, data):
        message_id = data['messageId']
        message = Message.objects.get(id=message_id)

        content = {
            'command': 'edit_message',
            'message': self.message_to_json(message)
        }

        return self.send_chat_message(content)

    
    def edited_message(self, data):
        message_id = data['messageId']
        message = Message.objects.get(id=message_id)
        message.body = data['message']
        message.save()

        content = {
            'command': 'edited_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def delete_message(self, data):
        message_id = data['messageId']
        message = Message.objects.get(id=message_id)
        elementId = data['elementId']

        content = {
            'command': 'delete_message',
            'elementId': elementId,
            'message': self.message_to_json(message)
        }
        return self.send_message(content) # YOU WILL HAVE TO CHECK THIS TO SEE IF THE SEND_CHAT_MESSAGE RATHER WILL NOT WORK FOR THIS

    def deleted_Message(self, data):
        message = Message.objects.get(id = data['messageId'])
        message.delete()
        elementId = data['elementId']


        content = {
            'command': 'send_chat_message',
            'elementId': elementId,
            'message': self.message_to_json(message),
            'roomid': data['roomid'],

        }
        return self.fetch_messages(content)

    def replyMessage(self, data):
        message = Message.objects.get(id = data['messageId'])


        content = {
            'command': 'reply_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)


    def replied_message(self, data):
        message = Message.objects.get(id = data['messageId'])
        user = User.objects.get(username=data['from'])
        user = user.profile
        message.replies = True
        reply = Reply.objects.create(
            message=message,
            reply=data['message'],
            user=user,
        )
        message.save()
        content = {
            'command': 'send_chat_message',
            'message': self.message_to_json(message),
            'roomid': data['roomid'],
        }
        return self.fetch_messages(content)


    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'new_image_message': new_image_message,
        'image_and_text': process_image_and_text,
        'editMessage': edit_message,
        'edited_message': edited_message,
        'deleteMessage': delete_message,
        'deleted_Message': deleted_Message,
        'replyMessage': replyMessage,
        'replied_message': replied_message,
    }


    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["pk"]
        self.room_group_name = f"chat_{self.room_name}"
    
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, 
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, 
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
                {
                "type": "chat_message",
                "message": message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))  

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps( message ))


# DAVID TAKE NOTITICE OF THIS, THE send_message IS USED TO SEND ALL THE MESSAGES, THAT IS THE MESSAGE THAT WILL BE PRELOADED UNTO THE CHAT BOX WHEN THE WEBSOCKET IS OPEN
# THE send_chat_message is used to send a single message when a user send or have a chat in the chat box. THIS IS GREAT MAN!
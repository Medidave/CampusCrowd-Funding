from django.db.models.signals import post_save, pre_delete, pre_save 
from django.dispatch import receiver
from .models import Message, Chat_forum 
from users.models import Project

from django.conf import settings 

import boto3
from urllib.parse import urlparse



@receiver(pre_delete, sender=Message)
def delete_chat_image(sender, instance, **kwargs):
    try:
         if instance.image:
            parsed_url = urlparse(instance.image.url)
            s3_object_key = parsed_url.path.lstrip('/')
            s3_object_key = s3_object_key.split('/')[-1]  # Split the path by '/', take the last element
            s3_object_key = 'message_images/' + s3_object_key  
            
        # Delete the message image or picture from S3
            session = boto3.Session(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )

            # Create S3 client with retrieved credentials
            s3_client = session.client('s3')
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME  
            try:
                s3_client.delete_object(Bucket=bucket_name, Key=s3_object_key)
            except Exception as e:
                print(f"Error deleting old profile picture: {e}")  # Handle the error here for Dave incase the ppicture was unable to be deleted from s3
    except sender.DoesNotExist:
        return  # No existing instance, nothing to delete
    
    
def create_Chat_forum(sender, instance, created, **kwargs):
    project = instance
    if created:
        Chat_forum.objects.create(
            host = project.project_owner,
            project = project,
            
        )

post_save.connect(create_Chat_forum, sender=Project)

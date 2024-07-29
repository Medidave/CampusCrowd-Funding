from django.db.models.signals import post_save, post_delete, pre_save 
from django.dispatch import receiver
from .models import Profile 
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.conf import settings 

import boto3

# @receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile.objects.create(
            user = user,
        )

        subject = 'WELCOME TO CampusCrowd'
        message = f"Hiiiii {user.first_name}\n\nWelcome to CampusCrowd, the dynamic platform where student and faculty ideas take flight!\n\nWe're thrilled to have you join our community of passionate individuals who are transforming the future.\n\nCampusCrowd"


        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )


def deleteUSer(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
        print('Deleting user...')
    except:
        pass


post_save.connect(createProfile, sender=User)
post_delete.connect(deleteUSer, sender=Profile) 


# THE BELOW CODE IS RESPONSIBLE FOR DELETIING A PROFILE PICTURE FROM S3 BUCKET WHEN A USER CHANGES HIS OR HER PROFILE PICTURE TO A NEW PICTURE
@receiver(pre_save, sender=Profile)
def delete_old_profile_picture(sender, instance, **kwargs):
    print("Dave the ceo 1\n\n")
    try:
        old_instance = sender.objects.get(id=instance.id)
        print("Dave the ceo 2\n\n")
    except sender.DoesNotExist:
        print("Dave the ceo 3\n\n")
        return  # No existing instance, nothing to delete

    if instance.profile_image != old_instance.profile_image:
        print("Dave the ceo 4\n\n")
        # Delete the old profile picture from S3
        if old_instance.profile_image and old_instance.profile_image != 'profiles/user-default.png':
            session = boto3.Session(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
            print("Dave the ceo 5\n\n")

            # Create S3 client with retrieved credentials
            s3_client = session.client('s3')
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME  
            s3_object_key = str(old_instance.profile_image)  

            try:
                s3_client.delete_object(Bucket=bucket_name, Key=s3_object_key)
                print("Dave the ceo last\n\n")
            except Exception as e:
                print(f"Error deleting old profile picture: {e}\n\n\n\n")  # Handle errors (optional)


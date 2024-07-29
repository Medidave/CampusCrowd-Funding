from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import uuid
import os

def decode_store_base64_image(image_data):
    extension = os.path.splitext(filename)[1].lower()  # Get extension (e.g., .png)
    filename = f'chat_image_{uuid.uuid4()}.jpg'  #{extension} Generate a unique filename
    with default_storage.open(filename, 'wb+') as destination:
        destination.write(image_data)

    # Save the URL to the database
    image_url = default_storage.url(filename)

    return image_url
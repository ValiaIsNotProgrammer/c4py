import uuid

from django.db import models

from api.users.models import User

def file_location(instance, filename, **kwargs):
    file_path = filename
    return file_path


class Screenshot(models.Model):
    # id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="screenshots")
    image = models.ImageField(upload_to=file_location)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(primary_key=True)

    class Meta:
        app_label = 'screenshot_service'


# class Message(models.Model):
#     user_id = models.IntegerField()
#     message = models.TextField()
#     uploaded_at = models.DateTimeField(auto_now_add=True)


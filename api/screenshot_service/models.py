import uuid

from rest_framework import serializers
from django.db import models


from api.users.models import User


class Screenshot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="screenshots")
    image = models.ImageField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(primary_key=True)
    whois = models.JSONField()

    class Meta:
        app_label = 'screenshot_service'


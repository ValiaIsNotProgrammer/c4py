from django.db import models

from api.users.models import User


class Screenshot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(primary_key=True)
    whois = models.JSONField()
    message_id = models.IntegerField()

    class Meta:
        app_label = 'screenshot_service'


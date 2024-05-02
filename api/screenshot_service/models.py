import uuid

from django.db import models

from users.models import User


class Screenshot(models.Model):
    """
    Модель для хранения сущности скриншота
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    whois = models.JSONField()
    message_id = models.IntegerField()
    process_time = models.FloatField()

    class Meta:
        app_label = 'screenshot_service'

    def __str__(self):
        return f"{self.id} - {self.image}"

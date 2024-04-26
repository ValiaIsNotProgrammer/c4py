from django.db import models


class Screenshot(models.Model):
    user_id = models.IntegerField()
    image = models.ImageField(upload_to='screenshots')
    uploaded_at = models.DateTimeField(auto_now_add=True)

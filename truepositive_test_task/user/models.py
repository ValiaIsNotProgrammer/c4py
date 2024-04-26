from django.db import models


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    language = models.CharField(max_length=10, choices=[('en', 'English'), ('ru', 'Russian')])
    screenshots = models.FileField(upload_to='screenshots')

    def __str__(self):
        return f'{self.user_id} - {self.language}'

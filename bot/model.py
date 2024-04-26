from django.db import models


class UserProfile(models.Model):
    user_id = models.IntegerField(primary_key=True)
    language = models.CharField(max_length=10, choices=[('en', 'English'), ('ru', 'Russian')])

    def __str__(self):
        return f'{self.user_id} - {self.language}'

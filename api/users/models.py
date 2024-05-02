from django.db import models


class User(models.Model):
    """
    Модель для хранения сущности скриншота
    """
    id = models.BigIntegerField(primary_key=True)
    language = models.CharField(max_length=10, choices=[('en', 'English'), ('ru', 'Russian')])

    class Meta:
        app_label = 'users'

    def __str__(self):
        return f'{self.id} - {self.language}'

from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True, editable=True)
    language = models.CharField(max_length=10, choices=[('en', 'English'), ('ru', 'Russian')])
    # screenshots = models.ManyToOneRel('screenshot_service.Screenshot', related_name='users', blank=True)

    class Meta:
        app_label = 'users'

    def __str__(self):
        return f'{self.id} - {self.language}'

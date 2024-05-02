from django.apps import AppConfig


class UserConfig(AppConfig):
    """
    Приложение для создания пользователей по ручке /users/
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

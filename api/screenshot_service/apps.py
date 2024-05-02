from django.apps import AppConfig


class ScreenshotServiceConfig(AppConfig):
    """
    Приложение для создания скриншотов по ручке /screenshots/
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'screenshot_service'


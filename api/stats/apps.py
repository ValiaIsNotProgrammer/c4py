from django.apps import AppConfig


class StatsConfig(AppConfig):
    """
    Приложение для создания краткой статистики по ручке /stats/
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stats'

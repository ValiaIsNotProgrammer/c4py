from datetime import date, timedelta
from typing import Union, Callable

from django.db.models import Avg, Count
from loguru import logger
from rest_framework import serializers

from screenshot_service.models import Screenshot
from users.models import User


class StatsSerializer(serializers.Serializer):
    all_users_count = serializers.IntegerField(required=False)
    all_screenshots_count = serializers.IntegerField(required=False)
    average_process_time = serializers.FloatField(required=False)
    average_len_screenshots_user = serializers.FloatField(required=False)
    count_screenshots_on_day = serializers.IntegerField(required=False)

    """
    Сериализатор для репрезентации JSON ответов
    Т.к. статистику мы не сохраняем в БД, то достаточно будет класс сериализатора для статистики
    """

    def to_representation(self, instance):
        """
        Метод для репрезентации и автоматического вычисления парамтерв статистики
        ВАЖНО: если ни одно поле статистики не указано, по-умолчанию возращаются все поля с вычисленными метриками
        переопределение в __init__ не подходит, т.к. super().to_representation(instance) вызывается во время него
        """
        data = super().to_representation(instance)
        if not data:
            data = self.set_all_stats_fields()
        logger.info("Serializing StatsSerializer {}".format(data))
        filtered_data = {}
        for field in data.keys():
            if data[field] is not None:
                logger.trace(f"{field}: {type(data[field])}")
                metric = self.calculate_metric(field)
                logger.trace(f"{field}: {metric}")
                filtered_data[field] = metric
        logger.info("Serialized StatsSerializer {}".format(filtered_data))
        return filtered_data

    def set_all_stats_fields(self):
        """
        Метод для явного указания активных полей статистики
        Используется по-умолчанию, если ни одно поле не выбрано
        """
        stats_fields = list(self.fields.fields.keys())
        data = {}
        for field in stats_fields:
            data[field] = True
        return data

    def calculate_metric(self, field: str) -> Union[int, float]:
        """
        Метод для вычисления метрики для поля сериализатора
        :param field:
        поле в сериализаторе статистики
        """
        metric_methods_dict = self.get_metric_methods(self, "get_metric_")
        for method in metric_methods_dict:
            if field in method:
                return metric_methods_dict[method]()

    def get_metric_all_users_count(self, *args, **kwargs):
        "Метод для вычисления всех пользователей"
        return User.objects.all().count()

    def get_metric_all_screenshots_count(self, *args, **kwargs):
        "Метод для вычисления всех скриншотов"
        return Screenshot.objects.all().count()

    def get_metric_average_process_time(self, *args, **kwargs):
        "Метод для вычисления арф. сред. для времени загрузки по каждый скриншотам"
        return Screenshot.objects.all().aggregate(avg=Avg('process_time'))['avg']

    def get_metric_average_len_screenshots_user(self, *args, **kwargs):
        "Метод для вычисления арф. сред. кол-ва скриншотов на каждого пользователя"
        queryset = User.objects.annotate(num_screenshots=Count('screenshot'))
        average_screenshots_per_user = queryset.aggregate(avg_screenshots=Avg('num_screenshots'))['avg_screenshots']
        return average_screenshots_per_user

    def get_metric_count_screenshots_on_day(self, *args, **kwargs):
        "Метод для вычисления кол-ва сделанных скриншотов на текущий день"
        return Screenshot.objects.filter(uploaded_at__day=date.today().day).all().count()

    @staticmethod
    def get_metric_methods(instance, metric_prefix: str) -> dict[str, Callable]:
        """
        Функция для возрата всех методов статистики
        Метод статистики определяется так, что имя метода должно начинаться на префикс metric_prefix
        """
        metrics_methods_dict = {}
        for method in dir(instance):
            if method.startswith(metric_prefix):
                metrics_methods_dict[method.replace(metric_prefix, "")] = getattr(instance, method)
        return metrics_methods_dict
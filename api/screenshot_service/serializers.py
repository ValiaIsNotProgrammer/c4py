from datetime import datetime

from loguru import logger
from rest_framework import serializers

from screenshot_service.models import Screenshot
from utils.screenshots import screenshot_maker


class ScreenshotSerializer(serializers.ModelSerializer):
    """
    Сериализатор для репрезентации JSON ответов
    """

    class Meta:
        model = Screenshot
        fields = ["image", "uploaded_at", "user", "url", "whois", "message_id", "process_time"]

    def __init__(self, *args, **kwargs):
        """
        При инициализации класса мы динамически меняем uploaded_at, process_time и image.name, т.к. создаем модель внутри ручки
        uploaded_at нам важно сделать здесь, т.к. потом она будет использоваться в image.name
        """
        super().__init__(*args, **kwargs)
        try:
            image = kwargs["data"]["image"]
            uploaded_at = datetime.now()
            kwargs["data"]["uploaded_at"] = uploaded_at.strftime("%Y-%m-%d %H:%M:%S")
            kwargs["data"]["process_time"] = round(kwargs["data"]["process_time"], 2)
            image.name = screenshot_maker.get_name_for_image(kwargs["data"])
        except KeyError:
            pass

    def create(self, validated_data: dict) -> Screenshot:
        """
        Метод переопределен в целях логгирования
        """
        logger.info("Creating screenshot")
        return Screenshot.objects.create(**validated_data)

    def validate(self, attrs):
        """
        Метод переопределен в целях логгирования
        """
        logger.info("Validating screenshot")
        return attrs

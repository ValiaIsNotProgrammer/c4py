from datetime import datetime

from loguru import logger
from rest_framework import serializers

from api.screenshot_service.models import Screenshot
from api.utils.screenshots import screenshot_maker


class ScreenshotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Screenshot
        fields = ["image", "uploaded_at", "user", "url", "whois", "message_id"]

    def __init__(self, *args, **kwargs):
        """
        При инициализации класса мы динамически меняем имя image
        """
        super().__init__(*args, **kwargs)
        try:
            image = kwargs["data"]["image"]
            uploaded_at = datetime.now()
            kwargs["data"]["uploaded_at"] = uploaded_at.strftime("%Y-%m-%d %H:%M:%S")
            image.name = screenshot_maker.get_name_for_image(kwargs["data"])
        except KeyError:
            pass

    def create(self, validated_data):
        logger.info("Creating screenshot")
        return Screenshot.objects.create(**validated_data)

    def validate(self, attrs):
        logger.info("Validating screenshot")
        return attrs

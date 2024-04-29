from loguru import logger
from rest_framework import serializers

from api.screenshot_service.models import Screenshot




class ScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screenshot
        fields = ["image", "uploaded_at", "user", "url", "whois"]

    def create(self, validated_data):
        logger.info("Creating screenshot")
        return Screenshot.objects.create(**validated_data)

    def validate(self, attrs):
        logger.info("Validating screenshot")
        return attrs

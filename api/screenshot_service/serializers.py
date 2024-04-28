from loguru import logger
from rest_framework import serializers

from api.screenshot_service.models import Screenshot
from api.users.serializers import UserSerializer
# from drf_extra_fields.fields import Base64ImageField


class ScreenshotSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    # image = Base64ImageField(required=False)
    # image_url = serializers.ImageField(required=False)
    class Meta:
        model = Screenshot
        fields = ["image", "uploaded_at", "user", "url"]

    def create(self, validated_data):
        logger.info("Creating screenshot")
        return Screenshot.objects.create(**validated_data)
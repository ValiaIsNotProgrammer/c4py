import json
import time

from loguru import logger
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from utils.screenshots import screenshot_maker

from .models import Screenshot
from .serializers import ScreenshotSerializer
from utils.whois import whois


class ScreenshotViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = Screenshot.objects.all()
    serializer_class = ScreenshotSerializer
    lookup_field = "image"

    """
    Класс viewset приложения screenshot_service (/screenshots/)
    """

    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        Метод для переопределения создании модели скриншота, т.к. поля image, whois, process_time создаются on-site
        """
        self.__validate_request_data(request.data)
        start_time = time.time()
        image = screenshot_maker.get_image(request.data.get('url'))
        end_time = time.time() - start_time
        if type(image) == str:
            return Response(data={'error': image}, status=status.HTTP_400_BAD_REQUEST)
        whois_json = json.dumps(whois.get_valid_whois_data(request.data.get('url')))
        serializer = ScreenshotSerializer(data={"url": request.data.get('url'),
                                                "image": image,
                                                "user": request.data.get('id'),
                                                "whois": whois_json,
                                                "message_id": request.data.get('message_id'),
                                                "process_time": float(end_time)})
        logger.info("Screenshot model created {}".format(serializer.__dict__))
        if serializer.is_valid():
            serializer.save()
            logger.success('Screenshot model saved')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def __validate_request_data(data: dict) -> None:
        """
        Метод для валидации необходимых для сериализатора полей в запросе
        """
        if not data["url"]:
            logger.error(f'Screenshot URL not found')
            raise ValidationError({'error': 'URL is required'})
        if not data["id"]:
            logger.error(f'User ID not found')
            raise ValidationError({'error': 'User ID is required'})
        if not data["message_id"]:
            logger.error(f'Message ID not found')
            raise ValidationError({'error': 'Message ID is required'})



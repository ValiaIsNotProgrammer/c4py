import io
import json
import os
from datetime import datetime

from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from loguru import logger
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet


from api.utils.screenshots import screenshot_maker

from .models import Screenshot
from .serializers import ScreenshotSerializer
from ..config import settings
from ..users.models import User
from api.utils.whois import whois



class ScreenshotViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = Screenshot.objects.all()
    serializer_class = ScreenshotSerializer
    lookup_field = "image"

    def _validate_request_data(self, data: dict):
        if not data["url"]:
            logger.error(f'Screenshot URL not found')
            raise ValidationError({'error': 'URL is required'})
        if not data["id"]:
            logger.error(f'User ID not found')
            raise ValidationError({'error': 'User ID is required'})

    def _get_exist(self, screenshot: Screenshot) -> Response:
        logger.success(f'Screenshot already exists, CACHED')
        data = screenshot.__dict__
        del data['_state']
        logger.warning("data['_state'] was deleted")
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        raw_url = request.data.get('url')
        url = screenshot_maker.to_correct(raw_url)
        # TODO: сделать так, чтобы API принимал только валидные ссылки. Обработку и корректировку URL должен делать клиент
        self._validate_request_data(request.data)
        screenshot = self.queryset.filter(url=url).first()
        if screenshot:
            return self._get_exist(screenshot)
        image = screenshot_maker.get_screenshot(url)
        whois_json = json.dumps(whois.get_valid_whois_data(url))
        serializer = ScreenshotSerializer(data={"url": url,
                                                "image": image,
                                                "user": request.data.get('id'),
                                                "whois": whois_json})
        logger.info("Screenshot model created")
        if serializer.is_valid():
            serializer.save()
            logger.success('Screenshot model saved')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# TODO: исправить локальную передачу файлов по url
# TODO: добавить логи
class ScreenshotImageViewSet(ListAPIView):
    queryset = Screenshot.objects.all()
    serializer_class = ScreenshotSerializer

    def get(self, request, path:str = None, *args, **kwargs):
        print('dsfasdffsfa')


def serve_media(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'))
    else:
        return HttpResponse('File not found', status=404)


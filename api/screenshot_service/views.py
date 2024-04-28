import io
import os

from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from loguru import logger
from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet

from api.utils.screenshots import screenshot_maker

from .models import Screenshot
from .serializers import ScreenshotSerializer
from ..config import settings
from ..users.models import User


class ScreenshotViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = Screenshot.objects.all()
    serializer_class = ScreenshotSerializer
    lookup_field = "image"

    def create(self, request, *args, **kwargs):
        raw_url = request.data.get('url')
        user_id = request.data.get('id')
        url = screenshot_maker.to_correct(raw_url)
        logger.trace(f'Screenshot url: {url}')
        if not url:
            logger.error(f'Screenshot url not found')
            return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not user_id:
            logger.error(f'User ID not found')
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        screenshot = self.queryset.filter(url=url)
        if screenshot:
            logger.success(f'Screenshot already exists, CACHED')
            data = screenshot[0].__dict__
            del data['_state']
            logger.warning("data['_state'] was deleted")
            return Response(data, status=status.HTTP_201_CREATED)
        screenshot_image_bytes = screenshot_maker.get_screenshot(url)
        user = get_object_or_404(User, id=user_id)
        domain = screenshot_maker.get_domain(url)
        filename = "screenshots/" + domain + ".png"
        image = ImageFile(io.BytesIO(screenshot_image_bytes), name=filename)
        serializer = ScreenshotSerializer(data={"url": url, "image": image,
                                                "user": user.id})
        logger.info("Screenshot model created: {}".format(serializer.data))
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
    print('adafdsfsd')
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'))
    else:
        return HttpResponse('File not found', status=404)


from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from loguru import logger
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(responses={404: 'User not found'})
    def retrieve(self, request, *args, **kwargs):
        "Метод переопределен для явного логирования"
        logger.info("Getting user {}".format(request.user.username))
        try:
            instance = self.get_object()
        except Http404:
            logger.error("User not found")
            return Response({'detail': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        logger.success("User {} retrieved successfully".format(request.user.username))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response

from stats.serializers import StatsSerializer
from users.models import User
from screenshot_service.models import Screenshot


class StatsListView(generics.RetrieveAPIView):
    serializer_class = StatsSerializer

    """
     Класс viewset приложения stats (/stats/)
     """

    @swagger_auto_schema(query_serializer=StatsSerializer)
    def get(self, request: Request, *args, **kwargs):
        """
         Метод для переопределения возращения сериализатора скриншота в зависимости от выбранных query
         Доступные query можно увидеть на /swagger/
         """
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)




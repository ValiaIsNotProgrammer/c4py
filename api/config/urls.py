from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users.views import UserViewSet
from screenshot_service.views import ScreenshotViewSet
from stats.views import StatsListView

from config.settings import MEDIA_URL, MEDIA_ROOT, DEBUG

schema_view = get_schema_view(
    openapi.Info(
        title="REST APIs",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ValiaChernykh@yandex.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'screenshots', ScreenshotViewSet)


urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('stats/', StatsListView.as_view(), name='stats'),
    path('', include(router.urls)),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

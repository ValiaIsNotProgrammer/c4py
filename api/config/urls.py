from django.conf.urls.static import static
from django.template.defaulttags import url
from django.urls import path, include
from django.views.static import serve
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api.users.views import UserViewSet
from api.screenshot_service.views import ScreenshotViewSet, serve_media, ScreenshotImageViewSet

from api.config.settings import MEDIA_URL, MEDIA_ROOT, DEBUG

schema_view = get_schema_view(
    openapi.Info(
        title="REST APIs",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'screenshots', ScreenshotViewSet)
# router.register(rf'media/screenshots/(?P<path>.+)/$', ScreenshotImageViewSet.as_view(), basename='media')


urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include(router.urls)),
    path(rf'media/screenshots/(?P<path>.+)/$', ScreenshotImageViewSet.as_view(), name='media')
    # path(MEDIA_URL+"/<path:path>/", serve_media, name='serve_media'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

# if DEBUG:
#     urlpatterns += [
#         url(r'^media/(?P<path>.*)$', serve, {
#             'document_root': MEDIA_ROOT,
#         }),
#     ]
print(urlpatterns)
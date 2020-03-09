from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rooms/", include("core.urls")),
    path("api/v1/rooms/", include("rooms.urls")),
    # path("api/v2/rooms/", include("rooms.urls_v2")),  # api 폴더 생성 후, urls_v1, views_v1 / urls_v2, views_v2
    path("api/v1/users/", include("users.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


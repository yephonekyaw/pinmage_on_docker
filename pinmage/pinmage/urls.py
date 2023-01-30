from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include

admin.autodiscover()

urlpatterns = [
    path("", include("pins.urls", namespace="pins")),
    path("account/", include("account.urls", namespace="account")),
    path("social-auth/", include('social_django.urls', namespace='social')),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)

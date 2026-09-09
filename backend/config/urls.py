from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("programs/", include("apps.programs.urls")),
    path("admissions/", include("apps.admissions.urls")),
    path("", include("apps.people.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

admin.site.site_header = "Sparsh Inclusive Education"
admin.site.site_title = "Sparsh Admin"
admin.site.index_title = "Content & admissions"

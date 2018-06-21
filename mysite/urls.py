from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from django.conf.urls.static import static
from materials.views import HomeView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^', include('construction.urls')),
    url(r'^', include('hr.urls')),
    url(r'^', include('materials.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

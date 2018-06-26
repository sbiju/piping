from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from django.conf.urls.static import static
from materials.views import HomeView
from control_centre.views import contact_us, Terms, Faq, AboutUs, Privacy


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('construction.urls')),
    url(r'^', include('control_centre.urls')),
    url(r'^', include('materials.urls')),
    url(r'^', include('hr.urls')),
    url(r'^terms/$', Terms.as_view(), name='terms'),
    url(r'^faq/$', Faq.as_view(), name='faq'),
    url(r'^about/$', AboutUs.as_view(), name='about'),
    url(r'^privacy/$', Privacy.as_view(), name='privacy'),
    url(r'^contact/$', contact_us, name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

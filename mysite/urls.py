from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from control_centre.views import contact_us, Terms, Faq, AboutUs, Privacy, ReadMore, Instruction, HomeView, \
    Data_Entry, AdminPage, Client, FabEntry, QcEntry, HrEntry, ConstHead


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('construction.urls')),
    url(r'^', include('control_centre.urls')),
    url(r'^', include('materials.urls')),
    url(r'^', include('hr.urls')),
    url(r'^', include('reports.urls')),
    url(r'^terms/$', Terms.as_view(), name='terms'),
    url(r'^data/$', Data_Entry.as_view(), name='data'),
    url(r'^admin_view/$', AdminPage.as_view(), name='admin_page'),
    url(r'^client/$', Client.as_view(), name='client_page'),
    url(r'^ch_view/$', ConstHead.as_view(), name='ch_view'),
    url(r'^fab_entry/$', FabEntry.as_view(), name='fab_entry'),
    url(r'^qc_entry/$', QcEntry.as_view(), name='qc_entry'),
    url(r'^hr_entry/$', HrEntry.as_view(), name='hr_entry'),
    url(r'^faq/$', Faq.as_view(), name='faq'),
    url(r'^about/$', AboutUs.as_view(), name='about'),
    url(r'^privacy/$', Privacy.as_view(), name='privacy'),
    url(r'^contact/$', contact_us, name='contact'),
    url(r'^read_more/$', ReadMore.as_view(), name='read_more'),
    url(r'^instruction/$', Instruction.as_view(), name='instruction'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

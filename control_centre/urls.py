from django.conf.urls import url
from .views import OwnerEditView, add_user, OwnerCreateView, login_view, logout_view, ProjectCreateView, \
    IsoCreateView, IsoListView, contact_us


urlpatterns = [
    url(r'^add_iso/$', IsoCreateView.as_view(), name='add_iso'),
    url(r'^add_project/$', ProjectCreateView.as_view(), name='add_project'),
    url(r'^edit_owner/(?P<pk>[\w-]+)/$', OwnerEditView.as_view(), name='edit_owner'),
    url(r'^add_owner/$', OwnerCreateView.as_view(), name='add_owner'),
    url(r'^iso_list/$', IsoListView.as_view(), name='iso_list'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^add_user/$', add_user, name='add_user'),
]
from django.conf.urls import url
from .views import add_user, OwnerCreateView, login_view, logout_view, ProjectCreateView, \
    IsoCreateView, IsoListView, UserAutocomplete, OwnerEditView, OwnerListView, iso_create, pipe_create


urlpatterns = [
    url(r'^add_iso/$', IsoCreateView.as_view(), name='add_iso'),
    url(r'^add_project/$', ProjectCreateView.as_view(), name='add_project'),
    url(r'^add/user/$', UserAutocomplete.as_view(), name='user_auto'),
    url(r'^owner/list/$', OwnerListView.as_view(), name='owner_list'),
    url(r'^add_owner/$', OwnerCreateView.as_view(), name='add_owner'),
    url(r'^add_pipe/$', pipe_create, name='add_pipe'),
    url(r'^edit_owner/(?P<pk>[\w-]+)/$', OwnerEditView.as_view(), name='edit_owner'),
    url(r'^iso_list/$', IsoListView.as_view(), name='iso_list'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^add_user/$', add_user, name='add_user'),
    url(r'^add/iso/$', iso_create, name='iso_add'),
]
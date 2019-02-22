from django.conf.urls import url
from .views import add_user, OwnerCreateView, login_view, logout_view, ProjectCreateView, \
    IsoCreateView, IsoListView, UserAutocomplete, OwnerEditView, OwnerListView, PipeCreateView, \
    MatListView, PipeEditView, IsoAutocomplete, UserListView, MatAutocomplete, ScheduleAutocomplete, \
    SizeAutocomplete, ServiceAutocomplete, LineClassAutocomplete, FittingCreateView, FlangeCreateView, \
    GradeAutocomplete, BoltCreateView, GasketMatAutocomplete, FlangeClassAutocomplete,GasketCreateView, \
    SpoolStatusAutocomplete, SpoolAddView, FitupAutocomplete, WeldAutocomplete, PefsAutocomplete, \
    search_iso, IsoDetailView, SpoolListView, SpoolUpdateView, search_spool, SpoolDetailView, IsoPrintView, \
    iso_export

from .sub_views import ServiceCreateView, SizeCreateView, MaterialCreateView, FlangeClassCreateView, \
    ScheduleCreateView, LineClassCreateView, GradeCreateView, GasketMaterialCreateView, SpoolStatusCreateView, \
    PefsAddView

urlpatterns = [
    url(r'^search/$', search_iso, name='search_iso'),
    url(r'^search_spool/$', search_spool, name='search_spool'),
    url(r'^add_iso/$', IsoCreateView.as_view(), name='add_iso'),
    url(r'^add_project/$', ProjectCreateView.as_view(), name='add_project'),
    url(r'^add_pefs/$', PefsAddView.as_view(), name='add_pefs'),
    url(r'^add/user/$', UserAutocomplete.as_view(), name='user_auto'),
    url(r'^user/list/$', UserListView.as_view(), name='user_list'),
    url(r'^owner/list/$', OwnerListView.as_view(), name='owner_list'),

    url(r'^add_owner/$', OwnerCreateView.as_view(), name='add_owner'),
    url(r'^add_pipe/$', PipeCreateView.as_view(), name='add_pipe'),
    url(r'^add_fitting/$', FittingCreateView.as_view(), name='add_fitting'),
    url(r'^add_flange/$', FlangeCreateView.as_view(), name='add_flange'),
    url(r'^add_bolt/$', BoltCreateView.as_view(), name='add_bolt'),
    url(r'^add_gasket/$', GasketCreateView.as_view(), name='add_gasket'),
    url(r'^add_spool/$', SpoolAddView.as_view(), name='add_spool'),
    url(r'^add_service/$', ServiceCreateView.as_view(), name='add_service'),
    url(r'^add_size/$', SizeCreateView.as_view(), name='add_size'),
    url(r'^add_material/$', MaterialCreateView.as_view(), name='add_material'),
    url(r'^add_flange_class/$', FlangeClassCreateView.as_view(), name='add_flange_class'),
    url(r'^add_schedule/$', ScheduleCreateView.as_view(), name='add_schedule'),
    url(r'^add_line_class/$', LineClassCreateView.as_view(), name='add_line_class'),
    url(r'^add_grade/$', GradeCreateView.as_view(), name='add_grade'),
    url(r'^add_gasket_material/$', GasketMaterialCreateView.as_view(), name='add_gasket_material'),
    url(r'^add_spool_status/$', SpoolStatusCreateView.as_view(), name='add_spool_status'),

    url(r'^edit_spool/(?P<pk>[\w-]+)/$', SpoolUpdateView.as_view(), name='edit_spool'),
    url(r'^edit_owner/(?P<pk>[\w-]+)/$', OwnerEditView.as_view(), name='edit_owner'),
    url(r'^iso_list/$', IsoListView.as_view(), name='iso_list'),
    url(r'^iso_pdf_list/$', IsoPrintView.as_view(), name='iso_pdf_list'),
    url(r'^iso_csv/$', iso_export, name='iso_csv'),
    url(r'^spool_list/$', SpoolListView.as_view(), name='spool_list'),
    url(r'^mat_list/$', MatListView.as_view(), name='mat_list'),
    url(r'^iso/(?P<pk>[\w-]+)/$', IsoDetailView.as_view(), name='iso_detail'),
    url(r'^spool/(?P<pk>[\w-]+)/$', SpoolDetailView.as_view(), name='spool_detail'),
    url(r'^edit_pipe/(?P<pk>[\w-]+)/$', PipeEditView.as_view(), name='edit_pipe'),

    url(r'^iso_auto/$', IsoAutocomplete.as_view(), name='iso_auto'),
    url(r'^pefs_auto/$', PefsAutocomplete.as_view(), name='pefs_auto'),
    url(r'^mat_auto/$', MatAutocomplete.as_view(), name='mat_auto'),
    url(r'^size_auto/$', SizeAutocomplete.as_view(), name='size_auto'),
    url(r'^service_auto/$', ServiceAutocomplete.as_view(), name='service_auto'),
    url(r'^sch_auto/$', ScheduleAutocomplete.as_view(), name='sch_auto'),
    url(r'^line_class_auto/$', LineClassAutocomplete.as_view(), name='line_auto'),
    url(r'^grade_auto/$', GradeAutocomplete.as_view(), name='grade_auto'),
    url(r'^gasket_auto/$', GasketMatAutocomplete.as_view(), name='gasket_auto'),
    url(r'^flange_auto/$', FlangeClassAutocomplete.as_view(), name='flange_auto'),
    url(r'^spool_auto/$', SpoolStatusAutocomplete.as_view(), name='spool_auto'),
    url(r'^fitup_auto/$', FitupAutocomplete.as_view(), name='fitup_auto'),
    url(r'^weld_auto/$', WeldAutocomplete.as_view(), name='weld_auto'),

    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^add_user/$', add_user, name='add_user'),

]
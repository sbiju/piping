from django.conf.urls import url
from .views import ProductionReport, IsoListView, SpoolListView, WelderReport, \
    DailyWeldReport

urlpatterns = [
    url(r'^project_iso_list/$', IsoListView.as_view(), name='project_iso_report'),
    url(r'^spool_report/$', SpoolListView.as_view(), name='spool_report'),
    url(r'^project_report/$', ProductionReport.as_view(), name='proj_report'),
    url(r'^welder_report/$', WelderReport.as_view(), name='welder_report'),
    url(r'^daily_weld_report/$', DailyWeldReport.as_view(), name='daily_weld_report'),
    ]
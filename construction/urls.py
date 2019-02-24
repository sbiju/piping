from django.conf.urls import url
from .views import JointListView, JointUpdateView, export, QcJointListView, QcJointUpdateView, \
    QcPrintView, qc_export, JointCreateView, JointPrintView, joint_export, QcCreateView, JointAutocomplete, \
    FitupListView, WeldedListView, NdtStatusAutocomplete, FitupPassedList, FitupFailList, WeldFailedList, \
    WeldPassedList, RadioFailedList, RadioPassedList, QcFitupUpdateView, QcWeldUpdateView


urlpatterns = [
    url(r'^joint_list/$', JointListView.as_view(), name='joint_list'),
    url(r'^fitup_list/$', FitupListView.as_view(), name='fitup_list'),
    url(r'^welded_list/$', WeldedListView.as_view(), name='welded_list'),
    url(r'^add_joints/$', JointCreateView.as_view(), name='joint_add'),
    url(r'^add_qc/$', QcCreateView.as_view(), name='qc_add'),
    url(r'^joint_auto/$', JointAutocomplete.as_view(), name='joint_auto'),
    url(r'^ndt_auto/$', NdtStatusAutocomplete.as_view(), name='ndt_auto'),
    url(r'^joints/(?P<pk>[\w-]+)/$', JointUpdateView.as_view(), name='joint_update'),
    url(r'^qc/joints/$', QcJointListView.as_view(), name='qc_joint_list'),
    url(r'^qc/fitup_passed/$', FitupPassedList.as_view(), name='fitup_passed'),
    url(r'^qc/fitup_failed/$', FitupFailList.as_view(), name='fitup_failed'),
    url(r'^qc/weld_passed/$', WeldPassedList.as_view(), name='weld_passed'),
    url(r'^qc/weld_failed/$', WeldFailedList.as_view(), name='weld_failed'),
    url(r'^qc/radio_failed/$', RadioFailedList.as_view(), name='radio_failed'),
    url(r'^qc/radio_passed/$', RadioPassedList.as_view(), name='radio_passed'),
    url(r'^qc/joints/(?P<pk>[\w-]+)/$', QcJointUpdateView.as_view(), name='qc_joint_update'),
    url(r'^qc/fitup/(?P<pk>[\w-]+)/$', QcFitupUpdateView.as_view(), name='qc_fitup_update'),
    url(r'^qc/welding/(?P<pk>[\w-]+)/$', QcFitupUpdateView.as_view(), name='qc_weld_update'),
    url(r'^fab/pdf/$', JointPrintView.as_view(), name='fab_pdf'),
    url(r'^fab/csv/$', joint_export, name='fab_csv'),
    url(r'^qc/pdf/$', QcPrintView.as_view(), name='qc_pdf'),
    url(r'^qc/csv/$', qc_export, name='qc_csv'),
    url(r'^csv/$', export, name='csv'),
]
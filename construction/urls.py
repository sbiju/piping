from django.conf.urls import url
from .views import JointListView, JointUpdateView, export, QcJointListView, QcJointUpdateView, \
    QcPrintView, qc_export, JointCreateView, JointPrintView, joint_export


urlpatterns = [
    url(r'^joints/$', JointListView.as_view(), name='joint_list'),
    url(r'^joints/add/$', JointCreateView.as_view(), name='joint_add'),
    url(r'^joints/(?P<pk>[\w-]+)/$', JointUpdateView.as_view(), name='joint_update'),
    url(r'^qc/joints/$', QcJointListView.as_view(), name='qc_joint_list'),
    url(r'^qc/joints/(?P<pk>[\w-]+)/$', QcJointUpdateView.as_view(), name='qc_joint_update'),
    url(r'^fab/pdf/$', JointPrintView.as_view(), name='fab_pdf'),
    url(r'^fab/csv/$', joint_export, name='fab_csv'),
    url(r'^qc/pdf/$', QcPrintView.as_view(), name='qc_pdf'),
    url(r'^qc/csv/$', qc_export, name='qc_csv'),
    url(r'^csv/$', export, name='csv'),

]
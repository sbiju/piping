from django.conf.urls import url
from .views import JointListView, JointUpdateView


urlpatterns = [
    url(r'^joints/$', JointListView.as_view(), name='joint_list'),
    url(r'^joints/(?P<pk>[\w-]+)/$', JointUpdateView.as_view(), name='joint_update'),

]
from django.conf.urls import url
from .views import OwnerCreateView


urlpatterns = [
    url(r'^add_owner/$', OwnerCreateView.as_view(), name='add_owner'),
    # url(r'^joints/(?P<pk>[\w-]+)/$', JointUpdateView.as_view(), name='joint_update'),

]
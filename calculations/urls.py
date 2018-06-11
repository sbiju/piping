from django.conf.urls import url
from .views import MaterialCreateView, DesignlListView, MaterialUpdateView, MaterialDetailView, \
    PurchaseListView, PurchaseUpdateView, MainListView


urlpatterns = [
    url(r'^add/$', MaterialCreateView.as_view(), name='add'),
    url(r'^add/(?P<pk>[\w-]+)/$', MaterialUpdateView.as_view(), name='update'),
    url(r'^design/$', DesignlListView.as_view(), name='design_list'),
    url(r'^main_list/$', MainListView.as_view(), name='main_list'),
    url(r'^list/(?P<pk>[\w-]+)/$', MaterialDetailView.as_view(), name='detail'),
    url(r'^purchase/$', PurchaseListView.as_view(), name='purchase_list'),
    url(r'^purchase/(?P<pk>[\w-]+)/$', PurchaseUpdateView.as_view(), name='purchase_update'),
]
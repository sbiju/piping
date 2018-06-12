from django.conf.urls import url
from .views import MaterialCreateView, DesignlListView, MaterialUpdateView, MaterialDetailView, \
    PurchaseListView, PurchaseUpdateView, MainListView, DesignUpdateView, StoreListView, StoreUpdateView,\
    FabListView, FabUpdateView, FabHomeView, FabStausView


urlpatterns = [
    url(r'^add/$', MaterialCreateView.as_view(), name='add'),
    url(r'^add/(?P<pk>[\w-]+)/$', MaterialUpdateView.as_view(), name='update'),
    url(r'^design/$', DesignlListView.as_view(), name='design_list'),
    url(r'^design/(?P<pk>[\w-]+)/$', DesignUpdateView.as_view(), name='design_update'),
    url(r'^main_list/$', MainListView.as_view(), name='main_list'),
    url(r'^list/(?P<pk>[\w-]+)/$', MaterialDetailView.as_view(), name='detail'),
    url(r'^purchase/$', PurchaseListView.as_view(), name='purchase_list'),
    url(r'^purchase/(?P<pk>[\w-]+)/$', PurchaseUpdateView.as_view(), name='purchase_update'),
    url(r'^store/$', StoreListView.as_view(), name='store_list'),
    url(r'^store/(?P<pk>[\w-]+)/$', StoreUpdateView.as_view(), name='store_update'),
    url(r'^fabrication/$', FabListView.as_view(), name='fab_list'),
    url(r'^fab_status/$', FabStausView.as_view(), name='fab_status'),
    url(r'^fabrication/(?P<pk>[\w-]+)/$', FabUpdateView.as_view(), name='fab_update'),
    url(r'^fab_dept/$', FabHomeView.as_view(), name='fab_home'),

]
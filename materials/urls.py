from django.conf.urls import url
from .views import MaterialCreateView, DesignlListView, MaterialUpdateView, MaterialDetailView, \
    PurchaseListView, PurchaseUpdateView, AdminListView, DesignUpdateView, StoreListView, StoreUpdateView,\
    FabListView, FabUpdateView, JointReportView, PerformReportView,\
    FabSumReportView, MyModelViewPrintView, FabDailyReportApiView, ProductionChartView, FabDailyReportAjaxView, \
    FabPrintView


urlpatterns = [
    url(r'^material/add/$', MaterialCreateView.as_view(), name='add'),
    url(r'^material/(?P<pk>[\w-]+)/$', MaterialUpdateView.as_view(), name='update'),
    url(r'^design/$', DesignlListView.as_view(), name='design_list'),
    url(r'^design/(?P<pk>[\w-]+)/$', DesignUpdateView.as_view(), name='design_update'),
    url(r'^main_list/$', AdminListView.as_view(), name='main_list'),
    url(r'^report_joint/$', JointReportView.as_view(), name='daily_joint_report'),
    url(r'^report_joint_pdf/$', FabPrintView.as_view(), name='report_joint_pdf'),
    url(r'^performance/$', PerformReportView.as_view(), name='perform_report'),

    # url(r'^report_iso/$', FabIsoReportView.as_view(), name='iso_fab_report'),
    # url(r'^report_daily/$', FabDailyReportView.as_view(), name='daily_fab_report'),
    url(r'^report_summary/$', FabSumReportView.as_view(), name='daily_sum_report'),
    url(r'^pdf/$', MyModelViewPrintView.as_view(), name='pdf_report'),
    url(r'^chart/$', ProductionChartView.as_view(), name='chart'),

    url(r'^list/(?P<pk>[\w-]+)/$', MaterialDetailView.as_view(), name='detail'),
    url(r'^purchase/$', PurchaseListView.as_view(), name='purchase_list'),
    url(r'^purchase/(?P<pk>[\w-]+)/$', PurchaseUpdateView.as_view(), name='purchase_update'),
    url(r'^store/$', StoreListView.as_view(), name='store_list'),
    url(r'^store/(?P<pk>[\w-]+)/$', StoreUpdateView.as_view(), name='store_update'),

    url(r'^api/fab/$', FabDailyReportApiView.as_view(), name='fab_api'),
    url(r'^report/fab/$', FabDailyReportAjaxView.as_view(), name='fab'),

    url(r'^fabrication/$', FabListView.as_view(), name='fab_list'),
    url(r'^fabrication/(?P<pk>[\w-]+)/$', FabUpdateView.as_view(), name='fab_update'),
    # url(r'^mat_add/$', material_create, name='material_add'),
]
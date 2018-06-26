from django.conf.urls import url
from .views import (EmployeeCreateView,
                    WelderCreateView,
                    EmployeeListView,
                    EmployeeAutocomplete,
                    FabricatorCreateView,
                    EngineerCreateView,
                    SupervisorCreateView,
                    EngineerListView,
                    SupervisorListView,
                    WelderListView,
                    FabricatorListView,
                    )


urlpatterns = [
    url(r'^employee_list/$', EmployeeListView.as_view(), name='employee_list'),
    url(r'^supervisor_list/$', SupervisorListView.as_view(), name='supervisor_list'),
    url(r'^welder_list/$', WelderListView.as_view(), name='welder_list'),
    url(r'^fabricator_list/$', FabricatorListView.as_view(), name='fabricator_list'),
    url(r'^engineer_list/$', EngineerListView.as_view(), name='engineer_list'),
    url(r'^add_employee/$', EmployeeCreateView.as_view(), name='add_employee'),
    url(r'^add_welder/$', WelderCreateView.as_view(), name='add_welder'),
    url(r'^add_engineer/$', EngineerCreateView.as_view(), name='add_engineer'),
    url(r'^add_supervisor/$', SupervisorCreateView.as_view(), name='add_supervisor'),
    url(r'^add_fabricator/$', FabricatorCreateView.as_view(), name='add_fabricator'),
    url(r'^employee_auto/$', EmployeeAutocomplete.as_view(), name='employee_auto'),
]
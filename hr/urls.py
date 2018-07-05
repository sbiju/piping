from django.conf.urls import url
from .views import (EmployeeCreateView,
                    EmployeeListView,
                    WelderAutocomplete,
                    FabricatorAutocomplete,
                    SupervisorAutocomplete,
                    EngineerAutocomplete,
                    EmpAutocomplete,
                    )


urlpatterns = [
    url(r'^employee_list/$', EmployeeListView.as_view(), name='employee_list'),
    url(r'^add_employee/$', EmployeeCreateView.as_view(), name='add_employee'),
    url(r'^welder_auto/$', WelderAutocomplete.as_view(), name='weld_auto'),
    url(r'^fab_auto/$', FabricatorAutocomplete.as_view(), name='fab_auto'),
    url(r'^sup_auto/$', SupervisorAutocomplete.as_view(), name='sup_auto'),
    url(r'^eng_auto/$', EngineerAutocomplete.as_view(), name='eng_auto'),
    url(r'^emp_auto/$', EmpAutocomplete.as_view(), name='emp_auto'),
]
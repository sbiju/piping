from django.conf.urls import url
from .views import (EmployeeCreateView,
                    EmployeeListView,
                    WelderAutocomplete,
                    FabricatorAutocomplete,
                    SupervisorAutocomplete,
                    EngineerAutocomplete,
                    EmpAutocomplete,
                    EmpPrintView,
                    qc_export,
                    RosterCreateView,
                    RosterListView,
                    DesignationAutocomplete
                    )


urlpatterns = [
    url(r'^employee_list/$', EmployeeListView.as_view(), name='employee_list'),
    url(r'^roster_list/$', RosterListView.as_view(), name='roster_list'),
    url(r'^add_employee/$', EmployeeCreateView.as_view(), name='add_employee'),
    url(r'^add_roster/$', RosterCreateView.as_view(), name='add_roster'),
    url(r'^welder_auto/$', WelderAutocomplete.as_view(), name='welder_auto'),
    url(r'^fabricator_auto/$', FabricatorAutocomplete.as_view(), name='fabricator_auto'),
    url(r'^sup_auto/$', SupervisorAutocomplete.as_view(), name='sup_auto'),
    url(r'^eng_auto/$', EngineerAutocomplete.as_view(), name='eng_auto'),
    url(r'^des_auto/$', DesignationAutocomplete.as_view(), name='des_auto'),
    url(r'^emp_auto/$', EmpAutocomplete.as_view(), name='emp_auto'),
    url(r'^employee/pdf/$', EmpPrintView.as_view(), name='emp_pdf'),
    url(r'^employee/csv/$', qc_export, name='emp_csv'),

]
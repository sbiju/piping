from django.shortcuts import render, redirect, Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Sum, Count
from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse_lazy
from dal import autocomplete
from django_weasyprint import WeasyTemplateResponseMixin

from materials.mixins import LoginRequiredMixin
from .models import Employee, Designation, DailyReport
from .forms import EmployeeCreateForm, RosterCreateForm
from control_centre.models import Owner, Project
from construction.resources import HrResource


class DesignationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Designation.objects.all()
        if self.q:
            qs = qs.filter(title__istartswith=self.q)
        return qs


class EmpAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Employee.objects.filter(project__owner__user=self.request.user)
        if self.q:
            qs = qs.filter(title__istartswith=self.q)
        return qs


class WelderAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Employee.objects.welders().filter(project__owner__user=self.request.user)
        if self.q:
            qs = qs.filter(first_name__istartswith=self.q)
        return qs


class FabricatorAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Employee.objects.fabricators().filter(project__owner__user=self.request.user)
        if self.q:
            qs = qs.filter(first_name__istartswith=self.q)
        return qs


class SupervisorAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Employee.objects.supervisors().filter(project__owner__user=self.request.user)
        if self.q:
            qs = qs.filter(first_name__istartswith=self.q)
        return qs


class EngineerAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Employee.objects.engineers().filter(project__owner__user=self.request.user)
        if self.q:
            qs = qs.filter(first_name__istartswith=self.q)
        return qs


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee

    def get_queryset(self):
        return Employee.objects.recent().filter(project__owner__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        context['headline'] = 'Employees List'
        return context


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeCreateForm
    template_name = 'forms/employee_form.html'
    success_url = reverse_lazy('add_employee')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        project = Project.objects.get(owner__user = self.request.user)
        form.instance.project = project
        valid_data = super(EmployeeCreateView, self).form_valid(form)
        return valid_data


class EmpPrintView(WeasyTemplateResponseMixin, ListView):
    model = Employee
    template_name = 'hr/emp_pdf_list.html'

    def get_queryset(self):
        return Employee.objects.recent().filter(project__owner__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(EmpPrintView, self).get_context_data(**kwargs)
        context['headline'] = 'Employees List'
        return context


def qc_export(request):
    user = request.user
    queryset = Employee.objects.filter(project__owner__user=user)
    qc_resource = HrResource().export(queryset)
    response = HttpResponse(qc_resource.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reports.xls"'
    return response


class RosterCreateView(LoginRequiredMixin, CreateView):
    model = DailyReport
    form_class = RosterCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('roster_list')

    def form_valid(self, form):
        # owner = Owner.objects.get(user=self.request.user)
        # form.instance.owner = owner
        project = Project.objects.get(owner__user=self.request.user)
        form.instance.project = project
        valid_data = super(RosterCreateView, self).form_valid(form)
        return valid_data

    # def get_object(self, *args, **kwargs):
    #     owner = Owner.objects.get(user=self.request.user)
    #     obj = super(WelderCreateView, self).get_object(*args, **kwargs)
    #     if obj.employee.project.owner == owner:
    #         return obj
    #     else:
    #         raise Http404


class RosterListView(LoginRequiredMixin, ListView):
    model = DailyReport

    def get_queryset(self):
        return DailyReport.objects.filter(project__owner__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(RosterListView, self).get_context_data(**kwargs)
        abs_list = DailyReport.objects.absent_emp().filter(project__owner__user=self.request.user)
        emp_list = Employee.objects.filter(project__owner__user=self.request.user).exclude(pk__in=abs_list)
        print(emp_list)
        context['object_list'] = DailyReport.objects.absent_emp().filter(project__owner__user=self.request.user)
        context['headline'] = 'Abscent List'
        return context
from django.shortcuts import render, redirect, Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Sum, Count
from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse_lazy
from dal import autocomplete

from .models import Employee, Designation
from .forms import EmployeeCreateForm
from control_centre.models import Owner, Project


class EmpAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Designation.objects.all()
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


class EmployeeListView(ListView):
    model = Employee

    def get_queryset(self):
        return Employee.objects.filter(project__owner__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        user = self.request.user
        context['headline'] = 'Employees'
        context['obj_list'] = Employee.objects.filter(project__owner__user=user)
        return context

#
# class EngineerListView(ListView):
#     model = Engineer
#
#     def get_queryset(self):
#         return Engineer.objects.filter(employee__project__owner__user=self.request.user)
#
#     def get_context_data(self, **kwargs):
#         context = super(EngineerListView, self).get_context_data(**kwargs)
#         user = self.request.user
#         context['obj_list'] = Engineer.objects.filter(employee__project__owner__user=user)
#         context['headline'] = 'Engineers'
#         return context
#
#
# class SupervisorListView(ListView):
#     model = Supervisor
#     template_name = 'hr/engineer_list.html'
#
#     def get_queryset(self):
#         return Supervisor.objects.filter(employee__project__owner__user=self.request.user)
#
#     def get_context_data(self, **kwargs):
#         context = super(SupervisorListView, self).get_context_data(**kwargs)
#         user = self.request.user
#         context['obj_list'] = Supervisor.objects.filter(employee__project__owner__user=user)
#         context['headline'] = 'Supervisors'
#         return context
#
#
# class WelderListView(ListView):
#     model = Welder
#     template_name = 'hr/engineer_list.html'
#
#     def get_queryset(self):
#         return Welder.objects.filter(employee__project__owner__user=self.request.user)
#
#     def get_context_data(self, **kwargs):
#         context = super(WelderListView, self).get_context_data(**kwargs)
#         user = self.request.user
#         context['obj_list'] = Welder.objects.filter(employee__project__owner__user=user)
#         context['headline'] = 'Welders'
#         return context
#
#
# class FabricatorListView(ListView):
#     model = Fabricator
#     template_name = 'hr/engineer_list.html'
#
#     def get_queryset(self):
#         return Fabricator.objects.filter(employee__project__owner__user=self.request.user)
#
#     def get_context_data(self, **kwargs):
#         context = super(FabricatorListView, self).get_context_data(**kwargs)
#         user = self.request.user
#         context['obj_list'] = Fabricator.objects.filter(employee__project__owner__user=user)
#         context['headline'] = 'Fabricators'
#         return context


class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('add_employee')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        project = Project.objects.get(owner__user = self.request.user)
        form.instance.project = project
        valid_data = super(EmployeeCreateView, self).form_valid(form)
        return valid_data


# class EngineerCreateView(CreateView):
#     model = Engineer
#     form_class = EngineerCreateForm
#     template_name = 'form.html'
#     success_url = reverse_lazy('add_engineer')
#
#     def form_valid(self, form):
#         owner = Owner.objects.get(user=self.request.user)
#         form.instance.employee.project.owner = owner
#         valid_data = super(EngineerCreateView, self).form_valid(form)
#         return valid_data
#
#
# class SupervisorCreateView(CreateView):
#     model = Supervisor
#     form_class = SupervisorCreateForm
#     template_name = 'form.html'
#     success_url = reverse_lazy('add_supervisor')
#
#     def form_valid(self, form):
#         owner = Owner.objects.get(user=self.request.user)
#         form.instance.employee.project.owner = owner
#         valid_data = super(SupervisorCreateView, self).form_valid(form)
#         return valid_data
#
#
# class FabricatorCreateView(CreateView):
#     model = Fabricator
#     form_class = FabricatorCreateForm
#     template_name = 'form.html'
#     success_url = reverse_lazy('add_fabricator')
#
#     def form_valid(self, form):
#         owner = Owner.objects.get(user=self.request.user)
#         form.instance.employee.project.owner = owner
#         valid_data = super(FabricatorCreateView, self).form_valid(form)
#         return valid_data
#
#
# class WelderCreateView(CreateView):
#     model = Welder
#     form_class = WelderCreateForm
#     template_name = 'form.html'
#     success_url = reverse_lazy('add_welder')
#
#     def form_valid(self, form):
#         owner = Owner.objects.get(user=self.request.user)
#         form.instance.employee.project.owner = owner
#         valid_data = super(WelderCreateView, self).form_valid(form)
#         return valid_data

    # def get_object(self, *args, **kwargs):
    #     owner = Owner.objects.get(user=self.request.user)
    #     obj = super(WelderCreateView, self).get_object(*args, **kwargs)
    #     if obj.employee.project.owner == owner:
    #         return obj
    #     else:
    #         raise Http404


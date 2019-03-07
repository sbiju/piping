from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.views.generic import CreateView, UpdateView, ListView, TemplateView, DetailView
from django.urls import reverse_lazy
from dal import autocomplete
from .forms import ServiceCreateForm, SizeCreateForm, MaterialCreateForm, FlangeClassCreateForm, \
    ScheduleCreateForm, LineClassCreateForm, GradeCreateForm, GasketMaterialCreateForm, SpoolStatusCreateForm, \
    PefsCreateForm, ValveTypeCreateForm, ValveEndTypeCreateForm, MaterialGradeCreateForm, UnitCreateForm

from .models import Owner, Iso, Project, Pipe, Material, Size, Service, Schedule, LineClass, Fitting, Flange, \
    Bolt, BoltGrade, FlangeClass, GasketMaterial, Gasket, Spool, SpoolStatus, FitUpStatus, \
    WeldStatus, Pefs, ValveType, ValveEnd, MaterialGrade, Unit
import json

User = get_user_model()


class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        project = Project.objects.get(owner__user = self.request.user)
        form.instance.project = project
        valid_data = super(ServiceCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(ServiceCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Service'
        return context


class UnitCreateView(CreateView):
    model = Unit
    form_class = UnitCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        project = Project.objects.get(owner__user = self.request.user)
        form.instance.project = project
        valid_data = super(UnitCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(UnitCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Service'
        return context
        

class SizeCreateView(CreateView):
    model = Size
    form_class = SizeCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        project = Project.objects.get(owner__user = self.request.user)
        form.instance.project = project
        valid_data = super(SizeCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(SizeCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Size'
        return context


class MaterialCreateView(CreateView):
    model = Material
    form_class = MaterialCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        project = Project.objects.get(owner__user = self.request.user)
        form.instance.project = project
        valid_data = super(MaterialCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(MaterialCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Material'
        return context


class FlangeClassCreateView(CreateView):
    model = FlangeClass
    form_class = FlangeClassCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        project = Project.objects.get(owner__user = self.request.user)
        form.instance.project = project
        valid_data = super(FlangeClassCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(FlangeClassCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Flange Class'
        return context


class ScheduleCreateView(CreateView):
    model = Schedule
    form_class = ScheduleCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        project = Project.objects.get(owner__user = self.request.user)
        form.instance.project = project
        valid_data = super(ScheduleCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(ScheduleCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Schedule'
        return context


class LineClassCreateView(CreateView):
    model = LineClass
    form_class = LineClassCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        project = Project.objects.get(owner__user = self.request.user)
        form.instance.project = project
        valid_data = super(LineClassCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(LineClassCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Line Class'
        return context


class GradeCreateView(CreateView):
    model = BoltGrade
    form_class = GradeCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        project = Project.objects.get(owner__user = self.request.user)
        form.instance.project = project
        valid_data = super(GradeCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(GradeCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add A New Bolt Grade'
        return context


class GasketMaterialCreateView(CreateView):
    model = GasketMaterial
    form_class = GasketMaterialCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        project = Project.objects.get(owner__user = self.request.user)
        form.instance.project = project
        valid_data = super(GasketMaterialCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(GasketMaterialCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Gasket Material'
        return context


class PefsAddView(CreateView):
    model = Pefs
    form_class = PefsCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        valid_data = super(PefsAddView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(PefsAddView, self).get_context_data(**kwargs)
        context['heading'] = 'Add PEFS/ P&ID'
        return context


class ValveTypeCreateView(CreateView):
    model = ValveType
    form_class = ValveTypeCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        project = Project.objects.get(owner__user = self.request.user)
        form.instance.project = project
        valid_data = super(ValveTypeCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(ValveTypeCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Valve Type'
        return context
        

class ValveEndTypeCreateView(CreateView):
    model = ValveEnd
    form_class = ValveEndTypeCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        project = Project.objects.get(owner__user = self.request.user)
        form.instance.project = project
        valid_data = super(ValveEndTypeCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(ValveEndTypeCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Valve Type'
        return context


class MaterialGradeCreateView(CreateView):
    model = MaterialGrade
    form_class = MaterialGradeCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        project = Project.objects.get(owner__user = self.request.user)
        form.instance.project = project
        valid_data = super(MaterialGradeCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(MaterialGradeCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Valve Type'
        return context        


class SpoolStatusCreateView(CreateView):
    model = SpoolStatus
    form_class = SpoolStatusCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        project = Project.objects.get(owner__user = self.request.user)
        form.instance.project = project
        valid_data = super(SpoolStatusCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(SpoolStatusCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Spool Status'
        return context
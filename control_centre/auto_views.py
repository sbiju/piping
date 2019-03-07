from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.views.generic import CreateView, UpdateView, ListView, TemplateView, DetailView
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from dal import autocomplete
from django_weasyprint import WeasyTemplateResponseMixin

from construction.resources import IsoResource
from .forms import UserForm, OwnerCreateForm, LoginForm, ProjectCreateForm, IsoCreateForm, ContactusForm,\
    PipeCreateForm, FittingCreateForm, FlangeCreateForm, BoltCreateForm, GasketCreateForm, \
    SpoolAddForm, ValveCreateForm, ElbowCreateForm

from .models import Owner, Iso, Project, Pipe, Material, Size, Service, Schedule, LineClass, Fitting, Flange, \
    Bolt, BoltGrade, FlangeClass, GasketMaterial, Gasket, Spool, SpoolStatus, FitUpStatus, \
    WeldStatus, Pefs, BoltSize, Valve, ValveEnd, ValveType, Elbow, Coupling, Tee, BranchFitting, Reducer, \
    MaterialGrade, Unit


class IsoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Iso.objects.filter(project__owner__user=self.request.user)
        if self.q:
            qs = qs.filter(iso_no__icontains=self.q)
        return qs


class MatAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Material.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class SizeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Size.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class BoltSizeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = BoltSize.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
        
        
class ValveTypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ValveType.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs        


class ValveEndTypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ValveEnd.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs   

class MaterialGradeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = MaterialGrade.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs      

class ServiceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Service.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class UnitAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Unit.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
        
        
class ScheduleAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Schedule.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class LineClassAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = LineClass.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class GradeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = BoltGrade.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class GasketMatAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = GasketMaterial.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class FlangeClassAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = FlangeClass.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class SpoolStatusAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = SpoolStatus.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class PefsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Pefs.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class FitupAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = FitUpStatus.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class WeldAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = WeldStatus.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs    
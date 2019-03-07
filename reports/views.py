from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView, View
from materials.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django_weasyprint import WeasyTemplateResponseMixin
from django.db.models import Sum
import datetime
from django.utils import timezone
from django.db.models import Count, Sum, Avg
from dal import autocomplete

from construction.models import Joint, Qc, NdtStatus
from construction.forms import JointForm, QcJointForm, QcFitupForm, QcWeldForm, QcRadioForm, FitupForm, WeldForm
from construction.resources import IsoResource, QcResource, JointResource
from control_centre.models import Owner, Iso, Spool
import json

from control_centre.models import Iso


class IsoListView(LoginRequiredMixin, ListView):
    model = Iso
    paginate_by = 15
    queryset = Iso.objects.all() 
    template_name = 'reports/iso_list.html'

    def get_queryset(self):
        return Iso.objects.filter(project__owner__user=self.request.user).order_by('service')

    def get_context_data(self, **kwargs):
        context = super(IsoListView, self).get_context_data(**kwargs)
        return context
        
        
class SpoolListView(LoginRequiredMixin, ListView):
    model = Spool
    template_name = 'reports/spool_report.html'
    
    def get_queryset(self):
        return Spool.objects.filter(iso__project__owner__user=self.request.user).order_by('iso__iso_no')
        
        
class ProductionReport(LoginRequiredMixin, ListView):
    model = Joint
    template_name = 'reports/production_report.html'

    def get_context_data(self, **kwargs):
        context = super(ProductionReport, self).get_context_data(**kwargs)
        user = self.request.user
        context['report'] = Joint.objects.filter(iso__project__owner__user=user)
        return context
        

class DailyWeldReport(LoginRequiredMixin, ListView):
    model = Joint
    template_name = 'reports/daily_weld_report.html'

    def get_context_data(self, **kwargs):
        context = super(DailyWeldReport, self).get_context_data(**kwargs)
        user = self.request.user
        context['day_report'] = Joint.objects.welded().filter(iso__project__owner__user=user).values('weld_date') \
            .order_by('-weld_date').annotate(total_inch=Sum('inch_dia')) \
            .annotate(no_of_welder=Count('weld_date')) \
            .annotate(avg_man_hours=Avg('man_hours')) \
            .annotate(avg_dia=Sum('inch_dia')/Count('weld_date'))
        context['unit_report'] = Joint.objects.welded().filter(iso__project__owner__user=user).values('iso__unit__name') \
            .order_by('iso__unit__name').annotate(total_inch=Sum('inch_dia')) \
            .annotate(no_of_welder=Count('weld_date')) \
            .annotate(avg_man_hours=Avg('man_hours')) \
            .annotate(avg_dia=Sum('inch_dia')/Count('weld_date'))    
        context['total_dia'] = Joint.objects.welded().filter(iso__project__owner__user=user).values('inch_dia') \
            .aggregate(Sum('inch_dia'))
        context['average_dia'] = Joint.objects.welded().filter(iso__project__owner__user=user).values('weld_date') \
            .order_by('-weld_date').aggregate(avg_dia=Sum('inch_dia')/Count('weld_date'))
        return context
        
        
class WelderReport(LoginRequiredMixin, ListView):
    model = Joint
    template_name = 'reports/welder_report.html'

    def get_context_data(self, **kwargs):
        context = super(WelderReport, self).get_context_data(**kwargs)
        user = self.request.user
        context['welding'] = Joint.objects.welded().filter(iso__project__owner__user=user) \
            .values('welder__first_name').order_by('welder__first_name').annotate(inch_dia=Sum('inch_dia'))
        return context
        #  context['engineer'] = Iso.objects.filter(project__owner__user=user).values('joint__engineer__first_name') \
        #     .order_by('joint__engineer').annotate(total_inch=Sum('joint__inch_dia')) \
        #     .annotate(actual_inch=Sum('joint__actual_inch_dia')) \
        #     .annotate(avg_man_hours=Avg('joint__man_hours'))
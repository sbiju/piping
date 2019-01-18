from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView, View
from materials.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django_weasyprint import WeasyTemplateResponseMixin
from django.db.models import Sum
import datetime
from django.utils import timezone
from dal import autocomplete

from .models import Joint, Qc
from .forms import JointForm, QcJointForm
from .resources import IsoResource, QcResource, JointResource
from control_centre.models import Owner, Iso


def export(request):
    user = request.user
    queryset = Joint.objects.filter(iso__project__owner__user=user)
    iso_resource = IsoResource().export(queryset)
    response = HttpResponse(iso_resource.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reports.xls"'
    return response


class JointListView(LoginRequiredMixin, ListView):
    model = Joint
    days_ago = timezone.now() - datetime.timedelta(days=5)
    queryset = Joint.objects.all()
    template_name = 'construction/joint_list.html'

    def get_context_data(self, **kwargs):
        context = super(JointListView, self).get_context_data(**kwargs)
        user = self.request.user
        days_ago = timezone.now() - datetime.timedelta(days=6)
        context['mat_list'] = Joint.objects.filter(iso__project__owner__user=user)\
            .by_range(start_date=days_ago, end_date=timezone.now())
        return context


class JointPrintView(WeasyTemplateResponseMixin, ListView):
    model = Joint
    queryset = Joint.objects.all()
    template_name = 'construction/fab_pdf_list.html'

    def get_context_data(self, **kwargs):
        context = super(JointPrintView, self).get_context_data(**kwargs)
        user = self.request.user
        context['mat_list'] = Joint.objects.filter(iso__project__owner__user=user)
        return context


def joint_export(request):
    user = request.user
    queryset = Joint.objects.filter(iso__project__owner__user=user)
    joint_resource = JointResource().export(queryset)
    response = HttpResponse(joint_resource.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reports.xls"'
    return response


class JointReportAjaxView(View):

    def get(self, request, *args, **kwargs):
        data = {}
        days = 7
        start_date = timezone.now() - datetime.timedelta(days=days-1)
        datetime_list = []
        labels = []
        for x in range(0, days):
            new_time = start_date + datetime.timedelta(days=x)
            datetime_list.append(new_time)
            labels.append(new_time.strftime('%a'))
        user = self.request.user
        report = Joint.objects.filter(iso__project__owner__user=user).values('joint__date_completed') \
            .annotate(completed_inch_dia=Sum('joint__inch_dia'))
        labels = ["Sun","Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        default_items = [12, 15, 25, 41, 12, 5]
        data = {'labels': labels, 'default': default_items,}
        return JsonResponse(data)


class JointCreateView(CreateView):
    model = Joint
    form_class = JointForm
    template_name = 'forms/joint_form.html'
    success_url = reverse_lazy('joint_list')

    def form_valid(self, form):
        # owner = Owner.objects.get(fabrication=self.request.user)
        owner = Owner.objects.get(user=self.request.user)
        form.instance.iso.project.owner = owner
        valid_data = super(JointCreateView, self).form_valid(form)
        return valid_data


class JointUpdateView(UpdateView):
    model = Joint
    form_class = JointForm
    template_name = 'form.html'
    success_url = reverse_lazy('joint_list')


class QcAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Qc.objects.filter(joint__iso__project__owner__user=self.request.user)
        iso = self.forwarded.get('iso', None)
        if iso:
            qs = qs.filter(iso=iso)
        if self.q:
            qs = qs.filter(joint__joint_no__istartswith=self.q)
        return qs


class QcJointListView(LoginRequiredMixin, ListView):
    model = Joint
    queryset = Joint.objects.all()
    template_name = 'construction/qc_joint_list.html'

    def get_context_data(self, **kwargs):
        context = super(QcJointListView, self).get_context_data(**kwargs)
        user = self.request.user
        context['mat_list'] = Joint.objects.filter(iso__project__owner__user=user)
        return context


class QcPrintView(WeasyTemplateResponseMixin, ListView):
    model = Joint
    queryset = Joint.objects.all()
    template_name = 'construction/qc_pdf_list.html'

    def get_context_data(self, **kwargs):
        context = super(QcPrintView, self).get_context_data(**kwargs)
        user = self.request.user
        context['mat_list'] = Joint.objects.filter(iso__project__owner__user=user)
        return context


def qc_export(request):
    user = request.user
    queryset = Joint.objects.filter(iso__project__owner__user=user)
    qc_resource = QcResource().export(queryset)
    response = HttpResponse(qc_resource.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reports.xls"'
    return response


class QcCreateView(CreateView):
    model = Qc
    form_class = QcJointForm
    template_name = 'form.html'
    success_url = reverse_lazy('joint_list')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.iso.project.owner = owner
        valid_data = super(QcCreateView, self).form_valid(form)
        return valid_data


class QcJointUpdateView(UpdateView):
    model = Qc
    form_class = QcJointForm
    template_name = 'form.html'
    success_url = reverse_lazy('qc_joint_list')
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView, View
from materials.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django_weasyprint import WeasyTemplateResponseMixin
from django.db.models import Sum
import datetime
from django.utils import timezone
from django.db.models import Count, Sum, Avg
from dal import autocomplete

from .models import Joint, Qc, NdtStatus
from .forms import JointForm, QcJointForm, QcFitupForm, QcWeldForm, QcRadioForm, FitupForm, WeldForm
from .resources import IsoResource, QcResource, JointResource
from control_centre.models import Owner, Iso
import json


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
    template_name = 'construction/joint_list.html'

    def get_context_data(self, **kwargs):
        context = super(JointListView, self).get_context_data(**kwargs)
        user = self.request.user
        days_ago = timezone.now() - datetime.timedelta(days=6)
        context['total_list'] = Joint.objects.filter(iso__project__owner__user=user)
        # context['total_list'] = Joint.objects.filter(iso__project__owner__user=user) \
        #     .values('iso', 'iso__iso_no') \
        #     .annotate(total_inch_dia=Sum('inch_dia'))
        # context['mat_list'] = Joint.objects.filter(iso__project__owner__user=user) \
        #     .by_range(start_date=days_ago, end_date=timezone.now())
        return context


class ProductionReportView(LoginRequiredMixin, ListView):
    model = Joint
    template_name = 'construction/daily_prod_report.html'

    def get_context_data(self, **kwargs):
        context = super(ProductionReportView, self).get_context_data(**kwargs)
        user = self.request.user
        context['report'] = Joint.objects.filter(iso__project__owner__user=user)
        return context
        
        
class ProductionReportSummary(LoginRequiredMixin, ListView):
    model = Joint
    template_name = 'construction/summary_report.html'

    def get_context_data(self, **kwargs):
        context = super(ProductionReportSummary, self).get_context_data(**kwargs)
        user = self.request.user
        context['weld_list'] = Joint.objects.welded().filter(iso__project__owner__user=user) \
            .values('iso__project') \
            .order_by('iso__project') \
            .annotate(total_joint=Count('joint_no')) \
            .annotate(avg_man_hours=Avg('man_hours')) \
            .annotate(total_inch_dia=Sum('inch_dia'))
        context['fitup_list'] = Joint.objects.filter(iso__project__owner__user=user) \
            .values('iso__project') \
            .order_by('iso__project') \
            .annotate(total_joint=Count('joint_no')) \
            .annotate(avg_man_hours=Avg('man_hours')) \
            .annotate(total_inch_dia=Sum('inch_dia'))    
        return context
        

class QcProductionReport(LoginRequiredMixin, ListView):
    model = Qc
    template_name = 'construction/qc_prod_report.html'

    def get_context_data(self, **kwargs):
        context = super(QcProductionReport, self).get_context_data(**kwargs)
        user = self.request.user
        context['joint_list'] = Qc.objects.filter(iso__project__owner__user=user)
        context['heading'] = 'Total Joint List'
        return context
        
        
class FitupListView(LoginRequiredMixin, ListView):
    model = Joint
    template_name = 'construction/fitup_list.html'

    def get_context_data(self, **kwargs):
        context = super(FitupListView, self).get_context_data(**kwargs)
        user = self.request.user
        context['done_list'] = Joint.objects.fitup_done().filter(iso__project__owner__user=user)
        context['heading'] = 'Fit-Up Completed List'
        return context


class WeldedListView(LoginRequiredMixin, ListView):
    model = Joint
    template_name = 'construction/fitup_list.html'

    def get_context_data(self, **kwargs):
        context = super(WeldedListView, self).get_context_data(**kwargs)
        user = self.request.user
        context['done_list'] = Joint.objects.welded().filter(iso__project__owner__user=user)
        context['heading'] = 'Fit-Up Completed List'
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


class JointDetailView(DetailView):
    model = Joint


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
    form_class = FitupForm
    template_name = 'forms/fitup_form.html'
    success_url = reverse_lazy('joint_list')

    def form_valid(self, form):
        # owner = Owner.objects.get(fabrication=self.request.user)
        owner = Owner.objects.get(user=self.request.user)
        form.instance.iso.project.owner = owner
        valid_data = super(JointCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(JointCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Joints'
        return context


class JointUpdateView(UpdateView):
    model = Joint
    form_class = WeldForm
    template_name = 'form.html'
    success_url = reverse_lazy('joint_list')


class WeldUpdateView(UpdateView):
    model = Joint
    form_class = WeldForm
    template_name = 'form.html'
    success_url = reverse_lazy('joint_list')


class JointAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Joint.objects.filter(iso__project__owner__user=self.request.user)
        iso = self.forwarded.get('iso', None)
        if iso:
            qs = qs.filter(iso=iso)
        if self.q:
            qs = qs.filter(joint_no__istartswith=self.q)
        return qs


class NdtStatusAutocomplete(autocomplete.Select2QuerySetView):
        def get_queryset(self):
            qs = NdtStatus.objects.all()
            if self.q:
                qs = qs.filter(name__istartswith=self.q)
            return qs


class QcJointListView(LoginRequiredMixin, ListView):
    model = Joint
    template_name = 'construction/qc_joint_list.html'

    def get_context_data(self, **kwargs):
        context = super(QcJointListView, self).get_context_data(**kwargs)
        user = self.request.user
        context['joint_list'] = Joint.objects.filter(iso__project__owner__user=user)
        context['heading'] = 'Joint List'
        return context
        

# class QcJointListView(LoginRequiredMixin, ListView):
#     model = Qc
#     template_name = 'construction/qc_joint_list.html'

#     def get_context_data(self, **kwargs):
#         context = super(QcJointListView, self).get_context_data(**kwargs)
#         user = self.request.user
#         context['joint_list'] = Qc.objects.filter(iso__project__owner__user=user)
#         context['heading'] = 'Inspection Completed Joint List'
#         return context


class FitupPassedList(LoginRequiredMixin, ListView):
    model = Qc
    template_name = 'construction/fitup_passed.html'

    def get_context_data(self, **kwargs):
        context = super(FitupPassedList, self).get_context_data(**kwargs)
        user = self.request.user
        context['joint_list'] = Qc.objects.fitup_passed().filter(iso__project__owner__user=user)
        context['heading'] = 'Fitup Passed Joint List'
        return context


class FitupFailList(LoginRequiredMixin, ListView):
    model = Qc
    template_name = 'construction/fitup_passed.html'

    def get_context_data(self, **kwargs):
        context = super(FitupFailList, self).get_context_data(**kwargs)
        user = self.request.user
        context['joint_list'] = Qc.objects.fitup_failed().filter(iso__project__owner__user=user)
        context['heading'] = 'Fitup Failed Joint List'
        return context


class WeldPassedList(LoginRequiredMixin, ListView):
    model = Qc
    template_name = 'construction/fitup_passed.html'

    def get_context_data(self, **kwargs):
        context = super(WeldPassedList, self).get_context_data(**kwargs)
        user = self.request.user
        context['joint_list'] = Qc.objects.welding_passed().filter(iso__project__owner__user=user)
        context['heading'] = 'Fitup Failed Joint List'
        return context


class WeldFailedList(LoginRequiredMixin, ListView):
    model = Qc
    template_name = 'construction/fitup_passed.html'

    def get_context_data(self, **kwargs):
        context = super(WeldFailedList, self).get_context_data(**kwargs)
        user = self.request.user
        context['joint_list'] = Qc.objects.welding_failed().filter(iso__project__owner__user=user)
        context['heading'] = 'Welding Failed Joint List'
        return context


class RadioPassedList(LoginRequiredMixin, ListView):
    model = Qc
    template_name = 'construction/fitup_passed.html'

    def get_context_data(self, **kwargs):
        context = super(RadioPassedList, self).get_context_data(**kwargs)
        user = self.request.user
        context['joint_list'] = Qc.objects.radiography_passed().filter(iso__project__owner__user=user)
        context['heading'] = 'Radiography Passed Joint List'
        return context


class RadioFailedList(LoginRequiredMixin, ListView):
    model = Qc
    template_name = 'construction/fitup_passed.html'

    def get_context_data(self, **kwargs):
        context = super(RadioFailedList, self).get_context_data(**kwargs)
        user = self.request.user
        context['joint_list'] = Qc.objects.radiography_failed().filter(iso__project__owner__user=user)
        context['heading'] = 'Radiography Failed Joint List'
        return context


class QcPrintView(WeasyTemplateResponseMixin, ListView):
    model = Joint
    queryset = Joint.objects.all()
    template_name = 'construction/qc_joint_list.html'

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
    success_url = reverse_lazy('qc_joint_list')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.iso.project.owner = owner
        valid_data = super(QcCreateView, self).form_valid(form)
        return valid_data


class QcFitupUpdateView(UpdateView):
    model = Qc
    form_class = QcFitupForm
    template_name = 'form.html'
    success_url = reverse_lazy('qc_joint_list')


class QcWeldUpdateView(UpdateView):
    model = Qc
    form_class = QcWeldForm
    template_name = 'form.html'
    success_url = reverse_lazy('qc_joint_list')


class QcRadioUpdateView(UpdateView):
    model = Qc
    form_class = QcRadioForm
    template_name = 'form.html'
    success_url = reverse_lazy('qc_joint_list')


class QcJointUpdateView(UpdateView):
    model = Qc
    form_class = QcJointForm
    template_name = 'form.html'
    success_url = reverse_lazy('qc_joint_list')


class QcJointDetailView(DetailView):
    model = Qc
    

def search_joint(request):
    query = request.GET.get('term', '')
    if query is not None:
        queryset = Joint.objects.search(query)
        res = [dict(id=iso.pk, label=[ iso.joint_no],
                value=iso.joint_no, url=iso.get_absolute_url())
                for iso in queryset]
        return HttpResponse(json.dumps(res))
    else:
        Joint.objects.none()
   
        
def search_qc(request):
    query = request.GET.get('term', '')
    if query is not None:
        queryset = Qc.objects.search(query)
        res = [dict(id=qc.pk, label=[ qc.joint],
                value=qc.joint, url=qc.get_absolute_url())
                for qc in queryset]
        return HttpResponse(json.dumps(res))
    else:
        Joint.objects.none()        
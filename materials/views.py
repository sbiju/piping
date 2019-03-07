from django.shortcuts import render, Http404
from django.db.models import Count, Sum, Avg
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView, View
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django_weasyprint import WeasyTemplateResponseMixin
import datetime
from django.utils import timezone
from django.forms import modelformset_factory

from .mixins import LoginRequiredMixin
from .models import MaterialData
from .forms import MaterialForm, PurchaseForm, DesignForm, StoreForm, FabForm
from control_centre.models import Owner, Iso
from construction.models import Joint

# administration
# class AdminListView(LoginRequiredMixin, ListView):
#     model = Iso
#     queryset = Iso.objects.all()
#     template_name = 'admn/material_list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(AdminListView, self).get_context_data(**kwargs)
#         user = self.request.user
#         context['mat_list'] = Iso.objects.filter(project__owner__user=user)
#         context['department'] = 'Administration Department'
#         context['sum_list'] = Iso.objects.filter(project__owner__user=user).values(
#             'materialdata__name',
#             'materialdata__size',
#             'materialdata__unit').order_by(
#             'materialdata__name',
#             'materialdata__size', ).annotate(total_quantity=Sum('materialdata__quantity'))
#         return context


# administration
class AdminListView(LoginRequiredMixin, ListView):
    model = MaterialData
    queryset = MaterialData.objects.all()
    template_name = 'admn/material_list.html'

    def get_context_data(self, **kwargs):
        context = super(AdminListView, self).get_context_data(**kwargs)
        user = self.request.user
        context['mat_list'] = Iso.objects.filter(project__owner__user=user)
        context['department'] = 'Administration Department'
        context['sum_list'] = MaterialData.objects.filter(iso__project__owner__user=user).values(
            'name',
            'size',
            'unit').order_by(
            'name',
            'size', ).annotate(total_quantity=Sum('quantity'))
        return context


# # administration
# class FabIsoReportView(LoginRequiredMixin, ListView):
#     model = Iso
#     queryset = Iso.objects.all()
#     template_name = 'admn/iso_report.html'

#     def get_context_data(self, **kwargs):
#         context = super(FabIsoReportView, self).get_context_data(**kwargs)
#         user = self.request.user
#         context['total'] = Iso.objects.filter(project__owner__user=user)

#         # context['report'] = Iso.objects.filter(project__owner__user=user).values('iso_no', 'inch_dia') \
#         #     .annotate(completed_inch_dia=Sum('joint__inch_dia'))
#         return context


class MyModelViewPrintView(WeasyTemplateResponseMixin, ListView):
    model = Iso
    template_name = 'admn/daily_fab_report.html'

    def get_context_data(self, **kwargs):
        context = super(MyModelViewPrintView, self).get_context_data(**kwargs)
        user = self.request.user
        context['date_report'] = Iso.objects.filter(project__owner__user=user).values('joint__date_completed') \
            .annotate(completed_inch_dia=Sum('joint__inch_dia'))
        return context


# fabrication
class FabDailyReportView(LoginRequiredMixin, ListView):
    model = Iso
    template_name = 'admn/daily_fab_report.html'
    
    def get_context_data(self, **kwargs):
        context = super(FabDailyReportView, self).get_context_data(**kwargs)
        user = self.request.user
        context['report'] = Iso.objects.filter(project__owner__user=user)
        context['sum_list'] = Iso.objects.filter(project__owner__user=user) \
            .values('project', 'project__name') \
            .annotate(total_joint=Count('joint__joint_no')) \
            .annotate(avg_man_hours=Avg('joint__man_hours')) \
            .annotate(total_inch_dia=Sum('joint__inch_dia'))
        context['date_report'] = Iso.objects.filter(project__owner__user=user).values('joint__date_completed') \
            .annotate(completed_inch_dia=Sum('joint__inch_dia'))    
        return context
    

# administration
class FabDailyReportAjaxView(View):

    def get(self, request, format=None):
        days = 7
        start_date = timezone.now().today() - datetime.timedelta(days=days-1)
        datetime_list = []
        labels = []
        dia_items = []
        for x in range(0, days):
            new_time = start_date + datetime.timedelta(days=x)
            datetime_list.append(new_time)
            labels.append(new_time.strftime('%a'))
            # dia_items.append(new_time.day)
            # print(dia_items)
        user = self.request.user
        qs = Joint.objects.filter(iso__project__owner__user=user)
        new_qs = qs.filter(date_completed__day=new_time.day, date_completed__month=new_time.month)
        print(new_qs)
        # day_total = new_qs.total_inch_dia()['inch_dia__sum']
        # if day_total is None:
        #     day_total=0
        # print(day_total)
        # dia_items.append(day_total)
        labels = labels
        dia_items = dia_items
        data = {'labels': labels, 'default': dia_items,}
        return JsonResponse(data)


# administration
class FabDailyReportApiView(APIView):

    def get(self, request, format=None):
        user = self.request.user
        report = Iso.objects.filter(project__owner__user=user).values('joint__date_completed') \
            .annotate(completed_inch_dia=Sum('joint__inch_dia'))
        return Response(report)


class ProductionChartView(TemplateView):
    template_name = 'admn/production_chart.html'


# administration
class FabSumReportView(LoginRequiredMixin, ListView):
    model = Iso
    queryset = Iso.objects.all()
    template_name = 'admn/fab_summary_report.html'

    def get_context_data(self, **kwargs):
        context = super(FabSumReportView, self).get_context_data(**kwargs)
        user = self.request.user
        context['sum_list'] = Iso.objects.filter(project__owner__user=user) \
            .values('project', 'project__name') \
            .annotate(completed_inch_dia=Sum('joint__inch_dia')) \
            .annotate(total_inch_dia=Sum('inch_dia'))
        return context


# administration
class JointReportView(LoginRequiredMixin, ListView):
    model = Iso
    template_name = 'admn/daily_joint_report.html'

    def get_context_data(self, **kwargs):
        context = super(JointReportView, self).get_context_data(**kwargs)
        user = self.request.user
        context['report'] = Iso.objects.filter(project__owner__user=user)
        context['sum_list'] = Iso.objects.filter(project__owner__user=user) \
            .values('project', 'project__name') \
            .annotate(total_joint=Count('joint__joint_no')) \
            .annotate(avg_man_hours=Avg('joint__man_hours')) \
            .annotate(total_inch_dia=Sum('joint__inch_dia'))
        return context


class FabPrintView(WeasyTemplateResponseMixin, ListView):
    model = Iso
    template_name = 'admn/daily_fab_report.html'

    def get_context_data(self, **kwargs):
        context = super(FabPrintView, self).get_context_data(**kwargs)
        user = self.request.user
        context['report'] = Iso.objects.filter(project__owner__user=user)
        context['sum_list'] = Iso.objects.filter(project__owner__user=user) \
            .values('project', 'project__name') \
            .annotate(total_joint=Count('joint__joint_no')) \
            .annotate(avg_man_hours=Avg('joint__man_hours')) \
            .annotate(total_inch_dia=Sum('joint__inch_dia'))
        return context


# administration
class PerformReportView(LoginRequiredMixin, ListView):
    model = Iso
    queryset = Iso.objects.all()
    template_name = 'admn/perform_report.html'

    def get_context_data(self, **kwargs):
        context = super(PerformReportView, self).get_context_data(**kwargs)
        user = self.request.user
        # context['welder'] = Iso.objects.filter(project__owner__user=user).values('joint__welder__first_name') \
        #     .order_by('joint__welder').annotate(total_inch=Sum('joint__inch_dia')) \
        #     .annotate(actual_inch=Sum('joint__actual_inch_dia'))
        context['welder'] = Joint.objects.welded().filter(iso__project__owner__user=user).values('welder__first_name') \
            .order_by('welder').annotate(total_inch=Sum('inch_dia')) \
            .annotate(actual_inch=Sum('actual_inch_dia'))
        context['fabricator'] = Joint.objects.welded().filter(iso__project__owner__user=user).values('fabricator__first_name') \
            .order_by('fabricator').annotate(total_inch=Sum('inch_dia')) \
            .annotate(actual_inch=Sum('actual_inch_dia'))
        context['supervisor'] = Joint.objects.welded().filter(iso__project__owner__user=user).values('supervisor__first_name') \
            .order_by('supervisor').annotate(total_inch=Sum('inch_dia')) \
            .annotate(actual_inch=Sum('actual_inch_dia')) \
            .annotate(avg_man_hours=Avg('man_hours'))
        context['engineer'] = Joint.objects.welded().filter(iso__project__owner__user=user).values('engineer__first_name') \
            .order_by('engineer').annotate(total_inch=Sum('inch_dia')) \
            .annotate(actual_inch=Sum('actual_inch_dia')) \
            .annotate(avg_man_hours=Avg('man_hours'))
        context['day_report'] = Joint.objects.welded().filter(iso__project__owner__user=user).values('weld_date') \
            .order_by('weld_date').annotate(total_inch=Sum('inch_dia')) \
            .annotate(actual_inch=Sum('actual_inch_dia')) \
            .annotate(avg_man_hours=Avg('man_hours'))    
        return context


# Design
class DesignlListView(LoginRequiredMixin, ListView):
    model = MaterialData
    queryset = MaterialData.objects.all()
    template_name = 'admn/material_list.html'

    def get_context_data(self, **kwargs):
        context = super(DesignlListView, self).get_context_data(**kwargs)
        user = self.request.user
        context['mat_list'] = Iso.objects.filter(project__owner__design=user)
        context['department'] = 'Design Department'
        context['sum_list'] = MaterialData.objects.filter(iso__project__owner__design=user).values(
            'name',
            'size',
            'unit').order_by(
            'name',
            'size', ).annotate(total_quantity=Sum('quantity'))
        return context


# Design
class MaterialCreateView(CreateView):
    model = MaterialData
    form_class = MaterialForm
    template_name = 'form.html'
    success_url = reverse_lazy('design_list')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        # owner = Owner.objects.get(design=self.request.user)
        # owner = MaterialData.objects.get(iso__project__owner__design=self.request.user)
        form.instance.iso.project.owner = owner
        valid_data = super(MaterialCreateView, self).form_valid(form)
        return valid_data


# def material_create(request):
#     materialFormset = modelformset_factory(Material, form=MaterialForm)
#     formset = materialFormset(request.POST or None, queryset=Material.objects.filter(iso__project__owner__user=request.user))
    

#     if formset.is_valid():
#         for form in formset:
#             obj = form.save(commit=False)
#             if form.cleaned_data:
#                 owner = Owner.objects.get(user=request.user)
#                 form.instance.iso.project.owner = owner
#                 obj.save()
#     context = {'formset': formset}
#     return render(request, 'formset.html', context)
#     # return HttpResponse('')


class PurchaseListView(ListView):
    model = MaterialData
    queryset = MaterialData.objects.all()
    template_name = 'purchase_list.html'

    def get_context_data(self, **kwargs):
        context = super(PurchaseListView, self).get_context_data(**kwargs)
        user = self.request.user
        context['mat_list'] = MaterialData.objects.filter(iso__project__owner__purchase=user)\
            .values('iso__iso_no',
                    'pk',
                    'name',
                    'size',
                    'price',
                    'quantity_purchased',
                    'total_price',
                    'balance_purchase')\
            .order_by('iso__iso_no',
                      'name',
                      'pk',
                      'size',
                      'price',
                      'quantity_purchased',
                      'total_price',
                      'balance_purchase')\
            .annotate(total_quantity=Sum('quantity'))
        return context


class StoreListView(ListView):
    model = MaterialData
    queryset = MaterialData.objects.all()
    template_name = 'store_list.html'

    def get_context_data(self, **kwargs):
        context = super(StoreListView, self).get_context_data(**kwargs)
        user = self.request.user
        context['mat_list'] = MaterialData.objects.filter(iso__project__owner__purchase=user)\
            .values('iso__iso_no','pk', 'name', 'size', 'quantity', 'quantity_issued', 'stock')\
            .order_by('iso__iso_no','name','pk', 'size', 'quantity', 'quantity_issued', 'stock')\
            .annotate(total_quantity=Sum('quantity'))
        return context


class FabListView(ListView):
    model = MaterialData
    queryset = MaterialData.objects.all()
    template_name = 'fab_list.html'

    def get_context_data(self, **kwargs):
        context = super(FabListView, self).get_context_data(**kwargs)
        user = self.request.user
        context['mat_list'] = MaterialData.objects.filter(iso__project__owner__purchase=user) \
            .values('iso__iso_no',
                    'pk',
                    'name',
                    'size',
                    'quantity',
                    'quantity_issued',
                    'stock',
                    'quantity_used',
                    'balance_used'
                    )\
            .annotate(total_quantity=Sum('quantity')) \
            .order_by('iso__iso_no',
                      'pk',
                      'name',
                      'size',
                      'quantity',
                      'quantity_issued',
                      'stock',
                      'quantity_used',
                      'balance_used'
                      )\
            .annotate(total_quantity=Sum('quantity'))
        return context


class MaterialDetailView(DetailView):
    model = MaterialData
    queryset = MaterialData.objects.all()
    template_name = 'detail.html'


class MaterialUpdateView(UpdateView):
    model = MaterialData
    form_class = MaterialForm
    template_name = 'form.html'
    success_url = reverse_lazy('design_list')

    def form_valid(self, form):
        owner = Owner.objects.get(design=self.request.user)
        form.instance.iso.project.owner = owner
        valid_data = super(MaterialUpdateView, self).form_valid(form)
        return valid_data


class DesignUpdateView(UpdateView):
    model = MaterialData
    form_class = DesignForm
    template_name = 'form.html'
    success_url = reverse_lazy('design_list')


class PurchaseUpdateView(UpdateView):
    model = MaterialData
    form_class = PurchaseForm
    template_name = 'form.html'
    success_url = reverse_lazy('purchase_list')


class StoreUpdateView(UpdateView):
    model = MaterialData
    form_class = StoreForm
    template_name = 'form.html'
    success_url = reverse_lazy('store_list')


class FabUpdateView(UpdateView):
    model = MaterialData
    form_class = FabForm
    template_name = 'form.html'
    success_url = reverse_lazy('fab_list')




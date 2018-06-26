from django.shortcuts import render, Http404
from django.db.models import Count, Sum, Avg
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView
from .mixins import LoginRequiredMixin
from .models import MaterialData
from .forms import MaterialForm, PurchaseForm, DesignForm, StoreForm, FabForm
from control_centre.models import Owner, Iso


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        # context['user_add'] = Owner.objects.filter(user=self.request.user)
        return context


class AdminHomeView(TemplateView):
    template_name = 'admn/admin_home.html'


class FabHomeView(TemplateView):
    template_name = 'fab_home.html'


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

# class AdminListView(LoginRequiredMixin, ListView):
#     model = Project
#     queryset = Project.objects.all()
#     template_name = 'admn/material_list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(AdminListView, self).get_context_data(**kwargs)
#         user = self.request.user
#         context['mat_list'] = Project.objects.filter(owner__user=user)
#         context['department'] = 'Administration Department'
#         context['sum_list'] = Project.objects.filter(owner__user=user).values(
#             'iso__materialdata__name',
#             'iso__materialdata__size',
#             'iso__materialdata__unit').order_by(
#             'iso__materialdata__name',
#             'iso__materialdata__size', ).annotate(total_quantity=Sum('iso__materialdata__quantity'))
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


# administration
class FabReportView(LoginRequiredMixin, ListView):
    model = Iso
    queryset = Iso.objects.all()
    template_name = 'admn/daily_fab_report.html'

    def get_context_data(self, **kwargs):
        context = super(FabReportView, self).get_context_data(**kwargs)
        user = self.request.user
        context['date_report'] = Iso.objects.filter(project__owner__user=user).values('joint__date_completed') \
            .annotate(completed_inch_dia=Sum('joint__inch_dia'))
        context['report'] = Iso.objects.filter(project__owner__user=user).values('iso_no', 'inch_dia') \
            .annotate(completed_inch_dia=Sum('joint__inch_dia'))
        context['sum_list'] = Iso.objects.filter(project__owner__user=user)\
            .values('project', 'project__name') \
            .annotate(completed_inch_dia=Sum('joint__inch_dia'))\
            .annotate(total_inch_dia=Sum('inch_dia'))
        return context


# administration
class JointReportView(LoginRequiredMixin, ListView):
    model = Iso
    queryset = Iso.objects.all()
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


# administration
class PerformReportView(LoginRequiredMixin, ListView):
    model = Iso
    queryset = Iso.objects.all()
    template_name = 'admn/perform_report.html'

    def get_context_data(self, **kwargs):
        context = super(PerformReportView, self).get_context_data(**kwargs)
        user = self.request.user
        context['welder'] = Iso.objects.filter(project__owner__user=user).values('joint__welder') \
            .order_by('joint__welder').annotate(total_inch=Sum('joint__inch_dia')) \
            .annotate(actual_inch=Sum('joint__actual_inch_dia'))
        context['fabricator'] = Iso.objects.filter(project__owner__user=user).values('joint__fabricator') \
            .order_by('joint__fabricator').annotate(total_inch=Sum('joint__inch_dia')) \
            .annotate(actual_inch=Sum('joint__actual_inch_dia'))
        context['supervisor'] = Iso.objects.filter(project__owner__user=user).values('joint__supervisor') \
            .order_by('joint__supervisor').annotate(total_inch=Sum('joint__inch_dia')) \
            .annotate(actual_inch=Sum('joint__actual_inch_dia')) \
            .annotate(avg_man_hours=Avg('joint__man_hours'))
        context['engineer'] = Iso.objects.filter(project__owner__user=user).values('joint__engineer') \
            .order_by('joint__engineer').annotate(total_inch=Sum('joint__inch_dia')) \
            .annotate(actual_inch=Sum('joint__actual_inch_dia')) \
            .annotate(avg_man_hours=Avg('joint__man_hours'))
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
        owner = Owner.objects.get(design=self.request.user)
        # owner = MaterialData.objects.get(iso__project__owner__design=self.request.user)
        form.instance.iso.project.owner = owner
        valid_data = super(MaterialCreateView, self).form_valid(form)
        return valid_data


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




from django.shortcuts import render, Http404
from django.db.models import Count, Sum
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, \
    CreateView, TemplateView
from .mixins import LoginRequiredMixin
from .models import MaterialData, Owner
from .forms import MaterialForm, PurchaseForm


class HomeView(TemplateView):
    template_name = 'home.html'

    # def get_context_data(self, **kwargs):
    #     context = super(HomeView, self).get_context_data(**kwargs)
    #     context['info_list'] = Info.objects.all()
    #     return context


class MainListView(LoginRequiredMixin, ListView):
    model = MaterialData
    queryset = MaterialData.objects.all()
    template_name = 'main_list.html'

    def get_context_data(self, **kwargs):
        context = super(MainListView, self).get_context_data(**kwargs)
        user = self.request.user
        context['mat_list'] = MaterialData.objects.filter(owner__user=user)\
            .values('iso__iso_no','name','pk', 'size','price', 'purchased', 'total_price', 'quantity')\
            .order_by('iso__iso_no','name','pk', 'size','price', 'purchased', 'total_price', 'quantity')\
            .annotate(total_quantity=Sum('quantity'))
        # context['tot_list'] = MaterialData.objects.filter(owner__designer=user).values('name', 'size').order_by('name', 'size') \
        #     .annotate(total_quantity=Sum('quantity'))
        return context


class DesignlListView(ListView):
    model = MaterialData
    queryset = MaterialData.objects.all()
    template_name = 'design_list.html'

    # def get_object(self, *args, **kwargs):
    #     user = self.request.user
    #     obj = super(MaterialListView, self).get_object(*args, **kwargs)
    #     if obj.user==user or user in obj.designer.all():
    #         return obj
    #     else:
    #         raise Http404

    def get_context_data(self, **kwargs):
        context = super(DesignlListView, self).get_context_data(**kwargs)
        user = self.request.user
        context['mat_list'] = MaterialData.objects.filter(owner__design=user).values('iso__iso_no','pk', 'name', 'size', 'quantity')\
            .order_by('iso__iso_no','name','pk', 'size', 'quantity').annotate(total_quantity=Sum('quantity'))
        context['tot_list'] = MaterialData.objects.filter(owner__design=user).values('name', 'size').order_by('name', 'size') \
            .annotate(total_quantity=Sum('quantity'))
        return context


class PurchaseListView(ListView):
    model = MaterialData
    queryset = MaterialData.objects.all()
    template_name = 'purchase_list.html'

    def get_context_data(self, **kwargs):
        context = super(PurchaseListView, self).get_context_data(**kwargs)
        user = self.request.user
        context['mat_list'] = MaterialData.objects.filter(owner__purchase=user).values('iso__iso_no','pk', 'name', 'size','price', 'purchased', 'total_price')\
            .order_by('iso__iso_no','name','pk', 'size','price', 'purchased', 'total_price').annotate(total_quantity=Sum('quantity'))
        # context['tot_list'] = MaterialData.objects.values('name', 'size').order_by('name', 'size') \
        #     .annotate(total_quantity=Sum('quantity'))
        return context


class MaterialDetailView(DetailView):
    model = MaterialData
    queryset = MaterialData.objects.all()
    template_name = 'detail.html'


class MaterialCreateView(CreateView):
    model = MaterialData
    form_class = MaterialForm
    template_name = 'form.html'
    success_url = reverse_lazy('main_list')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        valid_data = super(MaterialCreateView, self).form_valid(form)
        # form.instance.designer.add(user)
        return valid_data


class MaterialUpdateView(UpdateView):
    model = MaterialData
    form_class = MaterialForm
    template_name = 'form.html'
    success_url = reverse_lazy('main_list')

    # def get_object(self, *args, **kwargs):
    #     user = self.request.user
    #     owner = Owner.objects.get(user=self.request.user)
    #     obj = super(MaterialUpdateView, self).get_object(*args, **kwargs)
    #     try:
    #         if obj.owner==owner:
    #     except:
    #         pass
    #     try:
    #
    #         user in obj.owner__designer.all()
    #     except:
    #         pass
    #         return obj
    #     else:
    #         raise Http404


class PurchaseUpdateView(UpdateView):
    model = MaterialData
    form_class = PurchaseForm
    template_name = 'form.html'
    success_url = reverse_lazy('purchase_list')
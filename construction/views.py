from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView
from materials.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Joint
from .forms import JointForm


class JointListView(LoginRequiredMixin, ListView):
    model = Joint
    queryset = Joint.objects.all()
    template_name = 'joint_list.html'

    def get_context_data(self, **kwargs):
        context = super(JointListView, self).get_context_data(**kwargs)
        user = self.request.user
        context['mat_list'] = Joint.objects.filter(owner__fabrication=user)
        return context

class JointUpdateView(UpdateView):
    model = Joint
    form_class = JointForm
    template_name = 'form.html'
    success_url = reverse_lazy('joint_list')
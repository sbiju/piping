from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserForm, OwnerCreateForm
from .models import Owner


class OwnerCreateView(CreateView):
    model = Owner
    form_class = OwnerCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # owner = Owner.objects.get(user=self.request.user)
        form.instance.user = self.request.user
        valid_data = super(OwnerCreateView, self).form_valid(form)
        return valid_data


# def add_design_user(request):
#     form = UserForm(request.POST or None)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.user = Owner.objects.get(user=request.user)
#         instance.save()
#
#     return render(request, 'add_user.html', {})
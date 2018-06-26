from django.shortcuts import render, redirect, Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from .forms import UserForm, OwnerCreateForm, LoginForm, ProjectCreateForm, IsoCreateForm, ContactusForm
from .models import Owner, Iso, Project

User = get_user_model()


class ProjectCreateView(CreateView):
    model = Owner
    form_class = ProjectCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = Owner.objects.get(user=self.request.user)
        form.instance.owner = user
        try:
            return super(ProjectCreateView, self).form_valid(form)
        except IntegrityError:
            return HttpResponse('Your Project Exists!!')


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            HttpResponse('Invalid User')
    return render(request, 'login_form.html', {'form':form})


def logout_view(request):
    logout(request)
    return redirect('home')


class OwnerCreateView(CreateView):
    model = Owner
    form_class = OwnerCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super(OwnerCreateView, self).form_valid(form)
        except IntegrityError:
            return HttpResponse('Error! You are not authorized to perform this!!')


class OwnerEditView(UpdateView):
    model = Owner
    form_class = OwnerCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        valid_data = super(OwnerEditView, self).form_valid(form)
        return valid_data

    def get_object(self, *args, **kwargs):
        user = self.request.user
        obj = super(OwnerEditView, self).get_object(*args, **kwargs)
        if obj.user == user:
            return obj
        else:
            raise Http404


def add_user(request):
    form = UserForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create_user(username, email, password)
        return redirect('home')
    return render(request, 'form.html', context)


# Design
class IsoCreateView(CreateView):
    model = Iso
    form_class = IsoCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        project = Project.objects.get(owner__user = self.request.user)
        form.instance.project = project
        valid_data = super(IsoCreateView, self).form_valid(form)
        return valid_data


# Design
class IsoListView(ListView):
    model = Iso

    def get_queryset(self):
        return Iso.objects.filter(project__owner__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(IsoListView, self).get_context_data(**kwargs)
        user = self.request.user
        # context['headline'] = 'Employees'
        context['obj_list'] = Iso.objects.filter(project__owner__user=user)
        return context

class AboutUs(TemplateView):
    template_name = 'stat/about_us.html'


class Privacy(TemplateView):
    template_name = 'stat/privacy_policy.html'


class Terms(TemplateView):
    template_name = 'stat/terms.html'


class Faq(TemplateView):
    template_name = 'stat/faq.html'


def contact_us(request):
    form = ContactusForm(request.POST or None)
    if form.is_valid():
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")
        form_phone_number = form.cleaned_data.get("phone_number")
        subject = 'Blog contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email]
        contact_message = "%s/%s via %s/%s"%(
                form_full_name,
                form_message,
                form_email,
                form_phone_number
                )
        send_mail(subject,
                contact_message,
                from_email,
                to_email,
                fail_silently=False)
        messages.success(request, 'Thank you for contacting us, we will get back to you soon!')
        return redirect('home')

    context = {
        "form": form,
    }

    return render(request, 'stat/contact_us.html', context)
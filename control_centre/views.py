from django.shortcuts import render, redirect, Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib import messages
from dal import autocomplete

from .forms import UserForm, OwnerCreateForm, LoginForm, ProjectCreateForm, IsoCreateForm, ContactusForm
from .models import Owner, Iso, Project, Post

User = get_user_model()


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        post = Post.objects.all()
        context['post'] = post
        return context


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


class OwnerListView(ListView):
    model = Owner

    def get_queryset(self):
        return Owner.objects.filter(user=self.request.user)

    # def get_context_data(self, **kwargs):
    #     context = super(IsoListView, self).get_context_data(**kwargs)
    #     user = self.request.user
    #     # context['headline'] = 'Employees'
    #     context['obj_list'] = Iso.objects.filter(project__owner__user=user)
    #     return context


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
    success_url = reverse_lazy('owner_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super(OwnerEditView, self).form_valid(form)
        except IntegrityError:
            return HttpResponse('Error! You are not authorized to perform this!!')


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.filter(email=self.request.user.email)
        if self.q:
            qs = qs.filter(username__istartswith=self.q)
        return qs


def add_user(request):
    form = UserForm(request.POST or None)
    context = {'form': form}
    user_count = User.objects.filter(email=request.user.email).count()
    print(user_count)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = request.user.email
        password = form.cleaned_data.get('password')
        if not user_count > 7:
            new_user = User.objects.create_user(username, email, password)
        # else: raise messages.error(request, 'You have exceeded user limit')
        return redirect('add_user')
    return render(request, 'form.html', context)


# Design
class IsoCreateView(CreateView):
    # form_class = modelformset_factory(fields=['iso_no', 'no_of_joints', 'inch_dia'], model = Iso)
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


class ReadMore(TemplateView):
    template_name = 'stat/read_more.html'


class Instruction(TemplateView):
    template_name = 'stat/instructions.html'


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
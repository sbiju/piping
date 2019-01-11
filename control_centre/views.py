from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.views.generic import CreateView, UpdateView, ListView, TemplateView, DetailView
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib import messages
from dal import autocomplete
from django.db.models import Count, Sum, Avg, F, Case, When, IntegerField, Q
from django.forms.models import modelformset_factory
from queryset_sequence import QuerySetSequence
from .forms import UserForm, OwnerCreateForm, LoginForm, ProjectCreateForm, IsoCreateForm, ContactusForm,\
    PipeCreateForm, UserEditForm, FittingCreateForm, FlangeCreateForm, BoltCreateForm, GasketCreateForm, \
    SpoolAddForm, FabAddForm

from .models import Owner, Iso, Project, Pipe, Material, Size, Service, Schedule, LineClass, Fitting, Flange, \
    Bolt, BoltGrade, FlangeClass, GasketMaterial, Gasket, Spool, SpoolStatus, FabStatus, Fabrication, FitUpStatus, \
    WeldStatus
import json

User = get_user_model()


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
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


class UserListView(ListView):
    model = User
    template_name = 'control_centre/user_list.html'

    def get_queryset(self):
        return User.objects.filter(email=self.request.user.email)


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
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = request.user.email
        password = form.cleaned_data.get('password')
        if not user_count > 7:
            new_user = User.objects.create_user(username, email, password)
        # else: raise messages.error(request, 'You have exceeded user limit')
        return redirect('add_user')
    return render(request, 'form.html', context)


# from django.contrib.auth import update_session_auth_hash
#
# class UserEditView(UpdateView):
#     form_class = UserEditForm
#     template_name = 'form.html'
#     success_url = reverse_lazy('user_list')
#
#     def get_queryset(self):
#         return User.objects.filter(email=self.request.user.email)
#
#     def form_valid(self, form):
#         user = self.request.user
#         update_session_auth_hash(self, user)
#         try:
#             return super(UserEditView, self).form_valid(form)
#         except IntegrityError:
#             return HttpResponse('Error! You are not authorized to perform this!!')


# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('change_password')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'accounts/change_password.html', {
#         'form': form
#     })

# def edit_user(request, pk=None):
#     instance = get_object_or_404(User, pk=pk)
#     form = UserForm(request.POST or None, request.FILES or None, instance=instance)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.save()
#         return redirect('user_list')
#
#     context = {
#         "instance": instance,
#         "form":form,
#     }
#     return render(request, "post_form.html", context)

# Design
class IsoCreateView(CreateView):
    model = Iso
    form_class = IsoCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        project = Project.objects.get(owner__user = self.request.user)
        form.instance.project = project
        valid_data = super(IsoCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(IsoCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Iso'
        context['iso_count'] = Iso.objects.filter(project__owner__user=self.request.user).count()
        return context


class PipeCreateView(CreateView):
    model = Pipe
    form_class = PipeCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        valid_data = super(PipeCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(PipeCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Pipe'
        return context


class FlangeCreateView(CreateView):
    model = Flange
    form_class = FlangeCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        valid_data = super(FlangeCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(FlangeCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Flange'
        return context


class FittingCreateView(CreateView):
    model = Fitting
    form_class = FittingCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        valid_data = super(FittingCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(FittingCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Fitting'
        return context


class BoltCreateView(CreateView):
    model = Bolt
    form_class = BoltCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        valid_data = super(BoltCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(BoltCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Bolts/ Nuts'
        return context


class GasketCreateView(CreateView):
    model = Gasket
    form_class = GasketCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        valid_data = super(GasketCreateView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(GasketCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Gaskets'
        return context


class SpoolAddView(CreateView):
    model = Spool
    form_class = SpoolAddForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        valid_data = super(SpoolAddView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(SpoolAddView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Spool Name/ Number'
        return context


class FabAddView(CreateView):
    model = Fabrication
    form_class = FabAddForm
    template_name = 'form.html'
    success_url = reverse_lazy('data')

    def form_valid(self, form):
        owner = Owner.objects.get(user=self.request.user)
        form.instance.owner = owner
        valid_data = super(FabAddView, self).form_valid(form)
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(FabAddView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Fabrication Status'
        return context


class PipeEditView(UpdateView):
    model = Pipe
    form_class = PipeCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('pipe_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super(PipeEditView, self).form_valid(form)
        except IntegrityError:
            return HttpResponse('Error! You are not authorized to perform this!!')


class IsoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Iso.objects.filter(project__owner__user=self.request.user)
        if self.q:
            qs = qs.filter(iso_no__istartswith=self.q)
        return qs


class MatAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Material.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class SizeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Size.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class ServiceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Service.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class ScheduleAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Schedule.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class LineClassAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = LineClass.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class GradeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = BoltGrade.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class GasketMatAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = GasketMaterial.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class FlangeClassAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = FlangeClass.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class SpoolStatusAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = SpoolStatus.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class FabAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = FabStatus.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class FitupAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = FitUpStatus.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class WeldAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = WeldStatus.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


# Data
class IsoListView(ListView):
    model = Iso

    def get_queryset(self):
        return Iso.objects.filter(project__owner__user=self.request.user).order_by('service')

    def get_context_data(self, **kwargs):
        context = super(IsoListView, self).get_context_data(**kwargs)
        return context


class IsoDetailView(DetailView):
    model = Iso


class SpoolListView(ListView):
    model = Spool
    template_name = 'control_centre/spool_list.html'

    def get_queryset(self):
        return Spool.objects.filter(iso__project__owner__user=self.request.user).order_by('iso__iso_no')


class SpoolDetailView(DetailView):
    model = Spool
    template_name = 'control_centre/spool_detail.html'


class SpoolUpdateView(UpdateView):
    model = Spool
    form_class = SpoolAddForm
    template_name = 'forms/spool_form.html'
    success_url = reverse_lazy('spool_list')


class MatListView(ListView):
    model = Iso
    template_name = 'control_centre/mat_list.html'

    def get_queryset(self):
        return Iso.objects.filter(project__owner__user=self.request.user).order_by('service')

    def get_context_data(self, **kwargs):
        context = super(MatListView, self).get_context_data(**kwargs)
        return context


class Data_Entry(TemplateView):
    template_name = 'stat/data_entry.html'


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


def search_iso(request):
    query = request.GET.get('term', '')
    if query is not None:
        queryset = Iso.objects.search(query)
        res = [dict(id=iso.pk, label=[ iso.iso_no],
                value=iso.iso_no, url=iso.get_absolute_url())
                for iso in queryset]
        return HttpResponse(json.dumps(res))
    else:
        Iso.objects.none()


def search_spool(request):
    query = request.GET.get('term', '')
    if query is not None:
        queryset = Spool.objects.search(query)
        res = [dict(id=spool.pk, label=[ spool.spool_tag],
                value=spool.spool_tag, url=spool.get_absolute_url())
                for spool in queryset]
        return HttpResponse(json.dumps(res))
    else:
        Spool.objects.none()


'''
 # user = self.request.user
        # context['obj_list'] = Iso.objects.filter(project__owner__user=user)
        # qs1 = Iso.objects.filter(project__owner__user=user)\
        #     .values('service', 'pipe')\
        #     .annotate(pipe_length=Sum('pipe_1l'))
        # qs2 = Iso.objects.filter(project__owner__user=user) \
        #     .values('service', 'pipe2')\
        #     .annotate(pipe_length=Sum('pipe_2l'))
        # qs_fin = list(qs2) + list(qs1)
        # qs_3 = qs1.copy()
        # qs4 = qs_3.update(qs2)
        # qs_tot = Counter(qs1)+Counter(qs2)
        # len_tot = qs_tot.aggregate(pipe_l=Sum('pipe_length'))

        # len_tot = Iso.objects.filter(project__owner__user=user).values('service')\
        #     .filter(pipe=F('pipe2'))\
        #     .annotate(pipe_length=F('pipe_length') + F('pipe_length2'))

        # len_tot = Iso.objects.filter(project__owner__user=user)\
        #     .values('service','pipe','pipe2').annotate(
        #     pipe_length=Sum(
        #         Case(
        #             When(
        #                 pipe=F('pipe2'),
        #                 then=F('pipe_1l') + F('pipe_2l'),
        #             ),
        #             # When(
        #             #     ~Q(pipe=F('pipe2')),
        #             #     then=F('pipe_2l'),
        #             # ),
        #             # default=F('pipe_1l') and F('pipe_2l'),
        #             output_field=IntegerField(),
        #         ),
        #
        #     )
        # )
        #
        # print(qs_fin)
'''
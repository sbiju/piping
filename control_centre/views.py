from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.views.generic import CreateView, UpdateView, ListView, TemplateView, DetailView
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from dal import autocomplete
from django_weasyprint import WeasyTemplateResponseMixin
from materials.mixins import LoginRequiredMixin

from construction.resources import IsoResource
from .forms import UserForm, OwnerCreateForm, LoginForm, ProjectCreateForm, IsoCreateForm, ContactusForm,\
    PipeCreateForm, FittingCreateForm, FlangeCreateForm, BoltCreateForm, GasketCreateForm, \
    SpoolAddForm, ValveCreateForm, ElbowCreateForm, CouplingCreateForm, TeeCreateForm, ReducerCreateForm, \
    BrfCreateForm

from .models import Owner, Iso, Project, Pipe, Material, Size, Service, Schedule, LineClass, Fitting, Flange, \
    Bolt, BoltGrade, FlangeClass, GasketMaterial, Gasket, Spool, SpoolStatus, FitUpStatus, \
    WeldStatus, Pefs, BoltSize, Valve, ValveEnd, ValveType, Elbow, Coupling, Tee, BranchFitting, Reducer, \
    MaterialGrade

import json
User = get_user_model()


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
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


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'control_centre/user_list.html'

    def get_queryset(self):
        return User.objects.filter(email=self.request.user.email)


class OwnerCreateView(LoginRequiredMixin, CreateView):
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


class OwnerEditView(LoginRequiredMixin, UpdateView):
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
    return render(request, 'forms/user_form.html', context)


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
class IsoCreateView(LoginRequiredMixin, CreateView):
    model = Iso
    form_class = IsoCreateForm
    template_name = 'forms/iso_form.html'
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


class PipeCreateView(LoginRequiredMixin, CreateView):
    model = Pipe
    form_class = PipeCreateForm
    template_name = 'forms/pipe_form.html'
    success_url = reverse_lazy('data')

    # def form_valid(self, form):
    #     owner = Owner.objects.get(user=self.request.user)
    #     form.instance.owner = owner
    #     iso = Iso.objects.get(project__owner__user = self.request.user)
    #     form.instance.iso = iso
    #     valid_data = super(PipeCreateView, self).form_valid(form)
    #     return valid_data

    def get_context_data(self, **kwargs):
        context = super(PipeCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Pipe'
        return context


class FlangeCreateView(LoginRequiredMixin, CreateView):
    model = Flange
    form_class = FlangeCreateForm
    template_name = 'forms/flange_form.html'
    success_url = reverse_lazy('data')

    def get_context_data(self, **kwargs):
        context = super(FlangeCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Flange'
        return context


class FittingCreateView(LoginRequiredMixin, CreateView):
    model = Fitting
    form_class = FittingCreateForm
    template_name = 'forms/fitting_form.html'
    success_url = reverse_lazy('data')

    def get_context_data(self, **kwargs):
        context = super(FittingCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Fitting'
        return context


class BoltCreateView(LoginRequiredMixin, CreateView):
    model = Bolt
    form_class = BoltCreateForm
    template_name = 'forms/bolt_form.html'
    success_url = reverse_lazy('data')

    def get_context_data(self, **kwargs):
        context = super(BoltCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Bolts/ Nuts'
        return context


class ValveCreateView(LoginRequiredMixin, CreateView):
    model = Valve
    form_class = ValveCreateForm
    template_name = 'forms/valve_form.html'
    success_url = reverse_lazy('data')

    def get_context_data(self, **kwargs):
        context = super(ValveCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Valve'
        return context
        
        
class ElbowCreateView(LoginRequiredMixin, CreateView):
    model = Elbow
    form_class = ElbowCreateForm
    template_name = 'forms/elbow_form.html'
    success_url = reverse_lazy('data')

    def get_context_data(self, **kwargs):
        context = super(ElbowCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Fittings'
        return context
 
 
class TeeCreateView(LoginRequiredMixin, CreateView):
    model = Tee
    form_class = TeeCreateForm
    template_name = 'forms/elbow_form.html'
    success_url = reverse_lazy('data')

    def get_context_data(self, **kwargs):
        context = super(TeeCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Fittings'
        return context


class CouplingCreateView(LoginRequiredMixin, CreateView):
    model = Coupling
    form_class = CouplingCreateForm
    template_name = 'forms/elbow_form.html'
    success_url = reverse_lazy('data')

    def get_context_data(self, **kwargs):
        context = super(CouplingCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Fittings'
        return context
     
        
class ReducerCreateView(LoginRequiredMixin, CreateView):
    model = Reducer
    form_class = ReducerCreateForm
    template_name = 'forms/reducer_form.html'
    success_url = reverse_lazy('data')

    def get_context_data(self, **kwargs):
        context = super(ReducerCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Fittings'
        return context


class BrfCreateView(LoginRequiredMixin, CreateView):
    model = BranchFitting
    form_class = BrfCreateForm
    template_name = 'forms/elbow_form.html'
    success_url = reverse_lazy('data')

    def get_context_data(self, **kwargs):
        context = super(BrfCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Fittings'
        return context
        
        
class GasketCreateView(LoginRequiredMixin, CreateView):
    model = Gasket
    form_class = GasketCreateForm
    template_name = 'forms/gasket_form.html'
    success_url = reverse_lazy('data')

    def get_context_data(self, **kwargs):
        context = super(GasketCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Gaskets'
        return context


class SpoolAddView(LoginRequiredMixin, CreateView):
    model = Spool
    form_class = SpoolAddForm
    template_name = 'forms/spool_form.html'
    success_url = reverse_lazy('data')

    def get_context_data(self, **kwargs):
        context = super(SpoolAddView, self).get_context_data(**kwargs)
        context['heading'] = 'Add Spool Name/ Number'
        return context


class PipeEditView(LoginRequiredMixin, UpdateView):
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


# Data
class IsoListView(LoginRequiredMixin, ListView):
    model = Iso
    paginate_by = 15
    queryset = Iso.objects.all() 

    def get_queryset(self):
        return Iso.objects.filter(project__owner__user=self.request.user).order_by('service')

    def get_context_data(self, **kwargs):
        context = super(IsoListView, self).get_context_data(**kwargs)
        return context


class IsoPrintView(WeasyTemplateResponseMixin, ListView):
    model = Iso

    def get_queryset(self):
        return Iso.objects.filter(project__owner__user=self.request.user).order_by('service')


def iso_export(request):
    user = request.user
    queryset = Iso.objects.filter(project__owner__user=user)
    iso_resource = IsoResource().export(queryset)
    response = HttpResponse(iso_resource.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reports.xls"'
    return response


class IsoDetailView(LoginRequiredMixin, DetailView):
    model = Iso


class IsoEditView(LoginRequiredMixin, UpdateView):
    model = Iso
    form_class = IsoCreateForm
    template_name = 'forms/iso_form.html'
    success_url = reverse_lazy('iso_list')
    
    
class SpoolListView(LoginRequiredMixin, ListView):
    model = Spool
    template_name = 'control_centre/spool_list.html'

    def get_queryset(self):
        return Spool.objects.filter(iso__project__owner__user=self.request.user).order_by('-timestamp', 'iso__iso_no')


class SpoolDetailView(LoginRequiredMixin, DetailView):
    model = Spool
    template_name = 'control_centre/spool_detail.html'


class SpoolUpdateView(LoginRequiredMixin, UpdateView):
    model = Spool
    form_class = SpoolAddForm
    template_name = 'forms/spool_form.html'
    success_url = reverse_lazy('spool_list')


class MatListView(LoginRequiredMixin, ListView):
    model = Iso
    template_name = 'control_centre/mat_list.html'

    def get_queryset(self):
        return Iso.objects.filter(project__owner__user=self.request.user).order_by('service')

    def get_context_data(self, **kwargs):
        context = super(MatListView, self).get_context_data(**kwargs)
        return context


class MatDetailView(LoginRequiredMixin, DetailView):
    model = Iso
    

class Data_Entry(TemplateView):
    template_name = 'stat/data.html'


class FabEntry(TemplateView):
    template_name = 'stat/fabrication.html'

class QcEntry(TemplateView):
    template_name = 'stat/qc.html'    

class HrEntry(TemplateView):
    template_name = 'stat/hr.html'        
    
class AdminPage(TemplateView):
    template_name = 'stat/admin.html'

class Client(TemplateView):
    template_name = 'stat/client.html'

class ConstHead(TemplateView):
    template_name = 'stat/ch.html'


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
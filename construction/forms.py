from django import forms
from .models import Joint, Qc
from hr.models import Employee
from control_centre.models import Iso
from dal import autocomplete
from control_centre.models import Schedule, Size, FabStatus


class QcJointForm(forms.ModelForm):
    iso = forms.ModelChoiceField(
        queryset=Iso.objects.all(),
        widget=autocomplete.ModelSelect2(url='iso_auto')
    )
    joint = forms.ModelChoiceField(
        queryset=Qc.objects.all(),
        widget=autocomplete.ModelSelect2(url='qc_auto', forward=('iso',))

    )
    class Meta:
        model = Qc
        fields = ['iso', 'joint', 'hydro', 'radio', 'status', 'timestamp']


class JointForm(forms.ModelForm):
    iso = forms.ModelChoiceField(
        queryset=Iso.objects.all(),
        widget=autocomplete.ModelSelect2(url='iso_auto')
    )
    size = forms.ModelChoiceField(
        queryset=Size.objects.all(),
        widget=autocomplete.ModelSelect2(url='size_auto'),
    )
    sch = forms.ModelChoiceField(
        queryset=Schedule.objects.all(),
        widget=autocomplete.ModelSelect2(url='sch_auto'),
    )
    welder = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        widget=autocomplete.ModelSelect2(url='welder_auto')
    )
    fabricator = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        widget=autocomplete.ModelSelect2(url='fabricator_auto')
    )
    supervisor = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        widget=autocomplete.ModelSelect2(url='sup_auto')
    )
    engineer = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        widget=autocomplete.ModelSelect2(url='eng_auto')
    )
    erection_status = forms.ModelChoiceField(
        queryset=FabStatus.objects.all(),
        widget=autocomplete.ModelSelect2(url='fab_auto'),
    )
    fitup_status = forms.ModelChoiceField(
        queryset=FabStatus.objects.all(),
        widget=autocomplete.ModelSelect2(url='fab_auto'),
    )
    weld_status = forms.ModelChoiceField(
        queryset=FabStatus.objects.all(),
        widget=autocomplete.ModelSelect2(url='fab_auto'),
    )
    class Meta:
        model = Joint
        fields = ['iso', 'joint_no', 'size', 'sch', 'welder', 'fabricator',
                  'supervisor','engineer','hours_worked', 'crew_members', 'erection_status',
                  'fitup_status', 'weld_status']


# class JointForm(forms.ModelForm):
#     iso = forms.ModelChoiceField(
#         queryset=Iso.objects.all(),
#         widget=autocomplete.ModelSelect2(url='iso_auto')
#     )
#     welder = forms.ModelChoiceField(
#         queryset=Employee.objects.all(),
#         widget=autocomplete.ModelSelect2(url='welder_auto')
#     )
#     fabricator = forms.ModelChoiceField(
#         queryset=Employee.objects.all(),
#         widget=autocomplete.ModelSelect2(url='fabricator_auto')
#     )
#     supervisor = forms.ModelChoiceField(
#         queryset=Employee.objects.all(),
#         widget=autocomplete.ModelSelect2(url='sup_auto')
#     )
#     engineer = forms.ModelChoiceField(
#         queryset=Employee.objects.all(),
#         widget=autocomplete.ModelSelect2(url='eng_auto')
#     )
#     class Meta:
#         model = Joint
#         fields = ['iso', 'joint_no', 'size', 'sch', 'welder', 'fabricator',
#                   'supervisor','engineer','hours_worked', 'crew_members']


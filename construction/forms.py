from django import forms
from .models import Joint, Qc
from hr.models import Employee
from control_centre.models import Iso
from dal import autocomplete


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
    class Meta:
        model = Joint
        fields = ['iso', 'joint_no', 'size', 'sch', 'welder', 'fabricator',
                  'supervisor','engineer','hours_worked', 'crew_members']


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


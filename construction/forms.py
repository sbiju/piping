from django import forms
from .models import Joint, Qc
from hr.models import Employee
from control_centre.models import Iso
from dal import autocomplete
from control_centre.models import Schedule, Size, FitUpStatus, WeldStatus
from .models import NdtStatus


class DateInput(forms.DateInput):
    input_type = 'date'


class QcJointForm(forms.ModelForm):
    iso = forms.ModelChoiceField(
        queryset=Iso.objects.all(),
        widget=autocomplete.ModelSelect2(url='iso_auto')
    )
    fitup_status = forms.ModelChoiceField(
        queryset=NdtStatus.objects.all(),
        widget=autocomplete.ModelSelect2(url='ndt_auto')
    )
    welding_status = forms.ModelChoiceField(
        queryset=NdtStatus.objects.all(),
        widget=autocomplete.ModelSelect2(url='ndt_auto')
    )
    hydro_test_status = forms.ModelChoiceField(
        queryset=NdtStatus.objects.all(),
        widget=autocomplete.ModelSelect2(url='ndt_auto')
    )
    radiography_status = forms.ModelChoiceField(
        queryset=NdtStatus.objects.all(),
        widget=autocomplete.ModelSelect2(url='ndt_auto')
    )
    class Meta:
        model = Qc
        fields = ['iso', 'joint', 'fitup_status', 'fitup_inspection_date', 'welding_status',
                  'welding_inspection_date', 'hydro_test_status', 'hydro_test_inspection_date',
                  'radiography_status', 'radiography_inspection_date',]

        widgets = {
            'joint': autocomplete.ModelSelect2(url='joint_auto',
                                              forward=['iso']),
            'fitup_inspection_date': DateInput(),
            'welding_inspection_date': DateInput(),
            'hydro_test_inspection_date': DateInput(),
            'radiography_inspection_date': DateInput(),
        }


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
    fitup_status = forms.ModelChoiceField(
        queryset=FitUpStatus.objects.all(),
        widget=autocomplete.ModelSelect2(url='fitup_auto'),
    )
    weld_status = forms.ModelChoiceField(
        queryset=WeldStatus.objects.all(),
        widget=autocomplete.ModelSelect2(url='weld_auto'),
    )
    class Meta:

        model = Joint
        fields = ['date_completed', 'iso', 'joint_no', 'size', 'sch', 'welder', 'fabricator',
                  'supervisor','engineer','hours_worked', 'crew_members',
                  'fitup_status', 'weld_status', 'iso_comleted']

        widgets = {
            'date_completed': DateInput(),
        }


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


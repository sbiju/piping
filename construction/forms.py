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


class QcRadioForm(forms.ModelForm):
    iso = forms.ModelChoiceField(
        queryset=Iso.objects.all(),
        widget=autocomplete.ModelSelect2(url='iso_auto')
    )
    radiography_status = forms.ModelChoiceField(
        queryset=NdtStatus.objects.all(),
        widget=autocomplete.ModelSelect2(url='ndt_auto')
    )
    class Meta:
        model = Qc
        fields = ['iso', 'joint', 'radiography_status', 'radiography_inspection_date',]

        widgets = {
            'joint': autocomplete.ModelSelect2(url='joint_auto',
                                              forward=['iso']),
            'radiography_inspection_date': DateInput(),
        }


class QcWeldForm(forms.ModelForm):
    iso = forms.ModelChoiceField(
        queryset=Iso.objects.all(),
        widget=autocomplete.ModelSelect2(url='iso_auto')
    )
    welding_status = forms.ModelChoiceField(
        queryset=NdtStatus.objects.all(),
        widget=autocomplete.ModelSelect2(url='ndt_auto')
    )
    class Meta:
        model = Qc
        fields = ['iso', 'joint','fitup_status', 'welding_status', 'welding_inspection_date']

        widgets = {
            'joint': autocomplete.ModelSelect2(url='joint_auto',
                                              forward=['iso']),
            'welding_inspection_date': DateInput(),
        }

    def clean(self,*args,**kwargs):
        clean_form = super(QcWeldForm, self).clean()
        fitup_status = self.cleaned_data.get('fitup_status')
        print(fitup_status)
        fitup_instance = self.instance.fitup_status
        print(fitup_instance)
        if fitup_instance=='failed':
            raise forms.ValidationError("Fitup is not Passed")
        return clean_form

    # def clean_fitup_status(self,*args,**kwargs):
    #     fitup_status = self.cleaned_data.get('fitup_status')
    #     if fitup_status == 'failed':
    #         raise forms.ValidationError("Fitup is not Passed")
    #     print(fitup_status)
    #     return fitup_status


class QcFitupForm(forms.ModelForm):
    iso = forms.ModelChoiceField(
        queryset=Iso.objects.all(),
        widget=autocomplete.ModelSelect2(url='iso_auto')
    )
    fitup_status = forms.ModelChoiceField(
        queryset=NdtStatus.objects.all(),
        widget=autocomplete.ModelSelect2(url='ndt_auto')
    )
    class Meta:
        model = Qc
        fields = ['iso', 'joint', 'fitup_status', 'fitup_inspection_date']

        widgets = {
            'joint': autocomplete.ModelSelect2(url='joint_auto',
                                              forward=['iso']),
            'fitup_inspection_date': DateInput(),
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
                  'supervisor','engineer', 'crew_members',
                  'fitup_status', 'weld_status', 'iso_comleted']

        widgets = {
            'date_completed': DateInput(),
        }


class FitupForm(forms.ModelForm):
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

    class Meta:
        model = Joint
        fields = ['date_completed', 'iso', 'joint_no', 'size', 'sch', 'fabricator',
                  'supervisor','engineer','fitup_time', 'crew_members',
                  'fitup_status',]

        widgets = {
            'date_completed': DateInput(),
        }


class WeldForm(forms.ModelForm):
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
    weld_status = forms.ModelChoiceField(
        queryset=WeldStatus.objects.all(),
        widget=autocomplete.ModelSelect2(url='weld_auto'),
    )
    class Meta:
        model = Joint
        fields = ['date_completed', 'iso', 'joint_no', 'size', 'sch', 'welder',
                  'welding_time', 'crew_members',
                  'weld_status', 'iso_comleted']

        widgets = {
            'date_completed': DateInput(),
        }

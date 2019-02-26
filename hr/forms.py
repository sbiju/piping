from django import forms
from .models import Employee, Designation, DailyReport
from dal import autocomplete
from construction.forms import DateInput


class RosterCreateForm(forms.ModelForm):
    employee = forms.ModelChoiceField(
            queryset=Employee.objects.all(),
            widget=autocomplete.ModelSelect2(url='emp_auto')
        )
    class Meta:
        model = DailyReport
        fields = ['employee', 'absent', 'timestamp', ]
        widgets = {
            'timestamp': DateInput(),
        }


class EmployeeCreateForm(forms.ModelForm):
    designation = forms.ModelChoiceField(
        queryset=Designation.objects.all(),
        widget=autocomplete.ModelSelect2(url='des_auto')
    )

    class Meta:
        model = Employee
        fields = ['emplyee_no', 'first_name', 'last_name', 'designation', 'joined_date', ]



# class WelderCreateForm(forms.ModelForm):
#     employee = forms.ModelChoiceField(
#         queryset=Employee.objects.all(),
#         widget=autocomplete.ModelSelect2(url='employee_auto')
#     )
#
#     class Meta:
#
#         model = Welder
#         fields = ['employee']
#
#     def clean_employee(self):
#         employee = self.cleaned_data.get('employee')
#         qs = Welder.objects.filter(employee=employee)
#         if qs.exists():
#             raise forms.ValidationError("Error, This username already assigned as Welder")
#         qs_2 = Fabricator.objects.filter(employee=employee)
#         if qs_2.exists():
#             raise forms.ValidationError("Error, This username already assigned as Fabricator")
#         qs_3 = Supervisor.objects.filter(employee=employee)
#         if qs_3.exists():
#             raise forms.ValidationError("Error, This username already assigned as Supervisor")
#         qs_4 = Engineer.objects.filter(employee=employee)
#         if qs_4.exists():
#             raise forms.ValidationError("Error, This username already assigned as Engineer")
#         return employee




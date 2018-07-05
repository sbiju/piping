from django import forms
from .models import Employee, Designation
from dal import autocomplete


# class SupervisorCreateForm(forms.ModelForm):
#     employee = forms.ModelChoiceField(
#         queryset=Employee.objects.all(),
#         widget=autocomplete.ModelSelect2(url='employee_auto')
#     )
#
#     class Meta:
#         model = Supervisor
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
#
#
# class EngineerCreateForm(forms.ModelForm):
#     employee = forms.ModelChoiceField(
#         queryset=Employee.objects.all(),
#         widget=autocomplete.ModelSelect2(url='employee_auto')
#     )
#
#     class Meta:
#         model = Engineer
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
#
#
# class FabricatorCreateForm(forms.ModelForm):
#     employee = forms.ModelChoiceField(
#         queryset=Employee.objects.all(),
#         widget=autocomplete.ModelSelect2(url='employee_auto')
#     )
#
#     class Meta:
#         model = Fabricator
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
#
#
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


class EmployeeCreateForm(forms.ModelForm):
    designation = forms.ModelChoiceField(
        queryset=Designation.objects.all(),
        widget=autocomplete.ModelSelect2(url='emp_auto')
    )

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'emplyee_no', 'designation', 'joined_date', ]

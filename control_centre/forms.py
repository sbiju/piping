from django import forms
from .models import Owner, Project, Iso
from django.contrib.auth import get_user_model

User = get_user_model()


class IsoCreateForm(forms.ModelForm):

    class Meta:
        model = Iso
        fields = ['iso_no', 'no_of_joints', 'inch_dia', ]
        # labels = {'name': 'Project Name'}


class ProjectCreateForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name']
        labels = {'name': 'Project Name'}


class OwnerCreateForm(forms.ModelForm):

    class Meta:
        model = Owner
        fields = ['user', 'design', 'purchase', 'store', 'fabrication']
        labels = {'user': 'Admin'}


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError('This username already taken, please use a different one.')
        return username

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password_2 = self.cleaned_data.get('password_2')
        if password_2 != password:
            raise forms.ValidationError('Passsword doesn\'t match!!')
        return data


class ContactusForm(forms.Form):
    email = forms.EmailField()
    full_name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    phone_number = forms.IntegerField()

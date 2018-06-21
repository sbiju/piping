from django import forms
from .models import Owner


class OwnerCreateForm(forms.ModelForm):

    class Meta:
        model = Owner
        fields = ['user', 'design', 'purchase', 'store', 'fabrication']


class UserForm(forms.Form):
    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
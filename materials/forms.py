from django import forms
from .models import MaterialData, Iso


class DesignForm(forms.ModelForm):

    class Meta:
        model = MaterialData
        fields = ['iso', 'name', 'size', 'quantity', 'unit']


class StoreForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    size = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    quantity = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    class Meta:
        model = MaterialData
        fields = ['name', 'size', 'quantity', 'quantity_issued', 'stock', 'issued']


class PurchaseForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    size = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    quantity = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    class Meta:
        model = MaterialData
        fields = ['name', 'size', 'quantity', 'price','quantity_purchased']


class FabForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    size = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    quantity_issued = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    class Meta:
        model = MaterialData
        fields = ['name', 'size', 'quantity_issued', 'quantity_used','fabricated']



class MaterialForm(forms.ModelForm):

    class Meta:
        model = MaterialData
        fields = ['iso', 'name', 'size', 'quantity',]
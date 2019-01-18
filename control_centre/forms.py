from django import forms
from .models import Owner, Project, Iso, Pipe, Material, Size, Service, Schedule, LineClass, Fitting, Flange, \
    Bolt, BoltGrade, FlangeClass, GasketMaterial, Gasket, SpoolStatus, Spool, FabStatus, WeldStatus, \
    FitUpStatus

from django.contrib.auth import get_user_model
from dal import autocomplete


User = get_user_model()


class IsoCreateForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        widget=autocomplete.ModelSelect2(url='service_auto'),
    )
    line_class = forms.ModelChoiceField(
        queryset=LineClass.objects.all(),
        widget=autocomplete.ModelSelect2(url='line_auto'),
    )

    class Meta:
        model = Iso
        fields = ['iso_no',
                  'service',
                  'line_class',
                  'is_approved',
                  ]


class PipeCreateForm(forms.ModelForm):
    iso = forms.ModelChoiceField(
        queryset=Iso.objects.all(),
        widget=autocomplete.ModelSelect2(url='iso_auto'),
    )
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(),
        widget=autocomplete.ModelSelect2(url='mat_auto'),
    )

    size = forms.ModelChoiceField(
        queryset=Size.objects.all(),
        widget=autocomplete.ModelSelect2(url='size_auto'),
    )
    schedule = forms.ModelChoiceField(
        queryset=Schedule.objects.all(),
        widget=autocomplete.ModelSelect2(url='sch_auto'),
    )
    class Meta:
        model = Pipe
        fields = [ 'iso',
                   'size',
                   'material',
                   'schedule',
                   'length'
                  ]


class FittingCreateForm(forms.ModelForm):
    iso = forms.ModelChoiceField(
        queryset=Iso.objects.all(),
        widget=autocomplete.ModelSelect2(url='iso_auto'),
    )
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(),
        widget=autocomplete.ModelSelect2(url='mat_auto'),
    )

    size = forms.ModelChoiceField(
        queryset=Size.objects.all(),
        widget=autocomplete.ModelSelect2(url='size_auto'),
    )

    class Meta:
        model = Fitting
        fields = [ 'iso',
                   'name',
                   'size',
                   'material',
                   'quantity'
                  ]


class FlangeCreateForm(forms.ModelForm):
    iso = forms.ModelChoiceField(
        queryset=Iso.objects.all(),
        widget=autocomplete.ModelSelect2(url='iso_auto'),
    )
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(),
        widget=autocomplete.ModelSelect2(url='mat_auto'),
    )

    size = forms.ModelChoiceField(
        queryset=Size.objects.all(),
        widget=autocomplete.ModelSelect2(url='size_auto'),
    )
    flange_class = forms.ModelChoiceField(
        queryset=FlangeClass.objects.all(),
        widget=autocomplete.ModelSelect2(url='flange_auto'),
    )
    schedule = forms.ModelChoiceField(
        queryset=Schedule.objects.all(),
        widget=autocomplete.ModelSelect2(url='sch_auto'),
    )
    class Meta:
        model = Flange
        fields = [ 'iso',
                   'size',
                   'flange_class',
                   'material',
                   'schedule',
                   'quantity'
                  ]


class BoltCreateForm(forms.ModelForm):
    iso = forms.ModelChoiceField(
        queryset=Iso.objects.all(),
        widget=autocomplete.ModelSelect2(url='iso_auto'),
    )
    grade = forms.ModelChoiceField(
        queryset=BoltGrade.objects.all(),
        widget=autocomplete.ModelSelect2(url='grade_auto'),
    )

    size = forms.ModelChoiceField(
        queryset=Size.objects.all(),
        widget=autocomplete.ModelSelect2(url='size_auto'),
    )
    length = forms.ModelChoiceField(
        queryset=Size.objects.all(),
        widget=autocomplete.ModelSelect2(url='size_auto'),
    )
    class Meta:
        model = Bolt
        fields = [ 'iso',
                   'size',
                   'length',
                   'grade',
                   'quantity'
                  ]


class GasketCreateForm(forms.ModelForm):
    iso = forms.ModelChoiceField(
        queryset=Iso.objects.all(),
        widget=autocomplete.ModelSelect2(url='iso_auto'),
    )
    size = forms.ModelChoiceField(
        queryset=Size.objects.all(),
        widget=autocomplete.ModelSelect2(url='size_auto'),
    )
    gasket_class = forms.ModelChoiceField(
        queryset=FlangeClass.objects.all(),
        widget=autocomplete.ModelSelect2(url='flange_auto'),
    )
    gasket_material = forms.ModelChoiceField(
        queryset=GasketMaterial.objects.all(),
        widget=autocomplete.ModelSelect2(url='gasket_auto'),
    )
    class Meta:
        model = Gasket
        fields = [ 'iso',
                   'size',
                   'gasket_class',
                   'gasket_material',
                   'quantity'
                  ]


class SpoolAddForm(forms.ModelForm):
    iso = forms.ModelChoiceField(
        queryset=Iso.objects.all(),
        widget=autocomplete.ModelSelect2(url='iso_auto'),
    )
    spool_status = forms.ModelChoiceField(
        queryset=SpoolStatus.objects.all(),
        widget=autocomplete.ModelSelect2(url='spool_auto'),
    )
    # timestamp = forms.DateField(widget=DatePicker())
    class Meta:
        model = Spool
        fields = [ 'iso',
                   'spool_tag',
                   'spool_status',
                   'timestamp',
                  ]
        widgets = {
            'timestamp': forms.DateInput(attrs={'class': 'datepicker'}),
        }


class ServiceCreateForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ['name']


class SizeCreateForm(forms.ModelForm):

    class Meta:
        model = Size
        fields = ['name']


class MaterialCreateForm(forms.ModelForm):

    class Meta:
        model = Material
        fields = ['name']


class FlangeClassCreateForm(forms.ModelForm):

    class Meta:
        model = FlangeClass
        fields = ['name']


class ScheduleCreateForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = ['name']


class LineClassCreateForm(forms.ModelForm):

    class Meta:
        model = LineClass
        fields = ['name']


class GradeCreateForm(forms.ModelForm):

    class Meta:
        model = BoltGrade
        fields = ['name']


class GasketMaterialCreateForm(forms.ModelForm):

    class Meta:
        model = GasketMaterial
        fields = ['name']


class SpoolStatusCreateForm(forms.ModelForm):

    class Meta:
        model = SpoolStatus
        fields = ['name']


class ProjectCreateForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name']
        labels = {'name': 'Project Name'}


class OwnerCreateForm(forms.ModelForm):
    hr = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user_auto')
    )
    const_head = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user_auto')
    )
    design = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user_auto')
    )
    purchase = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user_auto')
    )
    store = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user_auto')
    )
    fabrication = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user_auto')
    )
    qc = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user_auto')
    )

    class Meta:
        model = Owner
        fields = ['const_head', 'hr', 'design', 'purchase', 'store', 'fabrication','qc']
        # labels = {'user': 'Admin'}


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserEditForm(forms.ModelForm):
   class Meta:
       model = User
       fields = ['username', 'password',]


class UserForm(forms.Form):
    username = forms.CharField()
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

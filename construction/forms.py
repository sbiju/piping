from django import forms
from .models import Joint


class JointForm(forms.ModelForm):

    class Meta:
        model = Joint
        fields = ['iso', 'joint_no', 'size', 'sch', 'welder', 'fabricator',
                  'hours_worked',]
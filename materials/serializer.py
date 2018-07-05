from rest_framework import serializers
from control_centre.models import Iso


class FabSerializer(serializers.ModelSerializer):

    class Meta:
        model = Iso
        fields = ['iso_no', 'no_of_joints', 'inch_dia']

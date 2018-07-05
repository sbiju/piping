from import_export import resources, fields
from .models import Joint


class IsoResource(resources.ModelResource):

    class Meta:
        model = Joint


class QcResource(resources.ModelResource):

    class Meta:
        model = Joint
        # fields = ('iso__iso_no', 'joint_no', 'size','sch', 'welder__employee__first_name', 'fabricator__employee__first_name', 'status', 'qc_checked')
        # export_order = ('iso__iso_no', 'joint_no', 'size','sch', 'welder__employee__first_name', 'fabricator__employee__first_name', 'status', 'qc_checked')
        # column_name = ('iso_no', 'joint_no', 'size','sch', 'welder_name', 'fabricator_name', 'status', 'qc_checked')
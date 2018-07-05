from import_export import resources, fields
from .models import Joint
from hr.models import Employee


class HrResource(resources.ModelResource):

    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'emplyee_no', 'designation__title', 'joined_date')


class IsoResource(resources.ModelResource):

    class Meta:
        model = Joint


class JointResource(resources.ModelResource):

    class Meta:
        model = Joint
        fields = ('iso__iso_no', 'joint_no', 'size', 'sch', 'welder__first_name',
                  'fabricator__first_name', 'supervisor__first_name', 'engineer__first_name',
                  'hours_worked', 'crew_members', 'date_completed','ndt', 'hydro','radio' )

        export_order = ('iso__iso_no', 'joint_no', 'size', 'sch', 'welder__first_name',
                      'fabricator__first_name', 'supervisor__first_name', 'engineer__first_name',
                      'hours_worked', 'crew_members', 'date_completed','ndt', 'hydro','radio' )


class QcResource(resources.ModelResource):

    class Meta:
        model = Joint
        fields = ('iso__iso_no', 'joint_no', 'size','sch', 'welder__first_name',
                  'fabricator__first_name', 'status', 'qc_checked')
        export_order = ('iso__iso_no', 'joint_no', 'size','sch', 'welder__first_name',
                        'fabricator__first_name', 'status', 'qc_checked')

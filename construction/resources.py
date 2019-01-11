from import_export import resources
from import_export.fields import Field
from .models import Joint
from hr.models import Employee


class HrResource(resources.ModelResource):
    first_name = Field(attribute='first_name', column_name='First Name')
    last_name = Field(attribute='last_name', column_name='Last Name')
    emplyee_no = Field(attribute='emplyee_no', column_name='Employee No.')
    designation__title = Field(attribute='designation__title', column_name='Designation')
    joined_date = Field(attribute='joined_date', column_name='Date of Joining')

    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'emplyee_no', 'designation__title', 'joined_date')
        export_order = ('emplyee_no', 'first_name', 'last_name', 'designation__title', 'joined_date')


class IsoResource(resources.ModelResource):

    class Meta:
        model = Joint


class JointResource(resources.ModelResource):
    iso__iso_no = Field(attribute='iso__iso_no', column_name='ISO No.')
    welder__first_name = Field(attribute='welder__first_name', column_name='Welder Name.')
    fabricator__first_name = Field(attribute='fabricator__first_name', column_name='Fabricator Name')
    supervisor__first_name = Field(attribute='supervisor__first_name', column_name='Supervisor Name')
    engineer__first_name = Field(attribute='engineer__first_name', column_name='Engineer Name')

    class Meta:
        model = Joint
        import_id_fields = ('iso__iso_no',)
        fields = ('iso__iso_no', 'joint_no', 'size', 'sch', 'welder__first_name',
                  'fabricator__first_name', 'supervisor__first_name', 'engineer__first_name',
                  'hours_worked', 'crew_members', 'date_completed' )

        export_order = ('iso__iso_no', 'joint_no', 'size', 'sch', 'welder__first_name',
                      'fabricator__first_name', 'supervisor__first_name', 'engineer__first_name',
                      'hours_worked', 'crew_members', 'date_completed')


class QcResource(resources.ModelResource):
    iso__iso_no = Field(attribute='iso__iso_no', column_name='ISO No.')
    welder__first_name = Field(attribute='welder__first_name', column_name='Welder Name.')
    fabricator__first_name = Field(attribute='fabricator__first_name', column_name='Fabricator Name')

    class Meta:
        model = Joint
        import_id_fields = ('iso__iso_no',)
        fields = ('iso__iso_no', 'joint_no', 'size','sch', 'welder__first_name',
                  'fabricator__first_name', 'status')
        export_order = ('iso__iso_no', 'joint_no', 'size','sch', 'welder__first_name',
                        'fabricator__first_name', 'status')

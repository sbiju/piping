from django.contrib import admin

from .models import Iso, Owner, Size, Fitting, Flange, Service, Pipe, Material, Schedule, LineClass, BoltGrade, \
    Bolt, FlangeClass, GasketMaterial, Gasket, SpoolStatus, Spool, FabStatus, FitUpStatus, WeldStatus

admin.site.register(FitUpStatus)
admin.site.register(WeldStatus)
admin.site.register(FabStatus)
admin.site.register(SpoolStatus)
admin.site.register(Spool)
admin.site.register(Gasket)
admin.site.register(FlangeClass)
admin.site.register(GasketMaterial)
admin.site.register(Bolt)
admin.site.register(BoltGrade)
admin.site.register(LineClass)
admin.site.register(Schedule)
admin.site.register(Material)
admin.site.register(Pipe)
admin.site.register(Owner)
admin.site.register(Iso)
admin.site.register(Size)
admin.site.register(Fitting)
admin.site.register(Flange)
admin.site.register(Service)
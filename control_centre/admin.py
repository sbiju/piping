from django.contrib import admin

from .models import Iso, Owner, Size, Fitting, Qty, Service, Pipe

admin.site.register(Pipe)
admin.site.register(Owner)
admin.site.register(Iso)
admin.site.register(Size)
admin.site.register(Fitting)
admin.site.register(Qty)
admin.site.register(Service)
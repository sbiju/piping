from django.contrib import admin

from .models import MaterialData, Iso, Owner


admin.site.register(Owner)
admin.site.register(MaterialData)
admin.site.register(Iso)

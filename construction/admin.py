from django.contrib import admin
from .models import Joint, Qc, NdtStatus


admin.site.register(NdtStatus)
admin.site.register(Qc)
admin.site.register(Joint)

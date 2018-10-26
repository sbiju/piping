from django.contrib import admin
from .models import  Employee, Project,Designation

admin.site.register(Designation)
admin.site.register(Project)
admin.site.register(Employee)
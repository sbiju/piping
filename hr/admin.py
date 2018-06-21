from django.contrib import admin
from .models import  Employee, Project, Owner, Welder, Fabricator, Engineer, Supervisor


admin.site.register(Welder)
admin.site.register(Fabricator)
admin.site.register(Engineer)
admin.site.register(Supervisor)
admin.site.register(Project)
admin.site.register(Owner)
admin.site.register(Employee)
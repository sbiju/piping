from django.contrib import admin

from .models import Post, Iso, Owner

admin.site.register(Owner)
admin.site.register(Post)
admin.site.register(Iso)
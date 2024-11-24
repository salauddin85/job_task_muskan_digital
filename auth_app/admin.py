from django.contrib import admin
from auth_app.models import CustomUser,Module

admin.site.register(CustomUser)
admin.site.register(Module)
# Register your models here.

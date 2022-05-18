from django.contrib import admin
from .models import CustomUserCreate
from django.contrib.auth.models import Group

class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username')

admin.site.register(CustomUserCreate, CustomUserAdmin)
admin.site.unregister(Group)

from django.contrib import admin
from django.contrib.auth.models import Group

from .models import CustomUserCreate, Follow


class CustomUserAdmin(admin.ModelAdmin):
    list_filter = (
        'email',
        'username'
    )
    search_fields = ('email', 'username',)
    empty_value_display = '-пусто-'


admin.site.register(CustomUserCreate, CustomUserAdmin)
admin.site.register(Follow)
admin.site.unregister(Group)

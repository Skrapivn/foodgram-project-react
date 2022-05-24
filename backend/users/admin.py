from django.contrib import admin
from django.contrib.auth.models import Group

from .models import CustomUserCreate, Follow


class CustomUserAdmin(admin.ModelAdmin):
    list_filter = (
        'pk',
        'email',
        'username',
        'first_name',
        'last_name',
    )
    search_fields = ('email', 'username',)
    list_filter = ('email', 'username',)
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'following',
    )
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'


admin.site.register(CustomUserCreate, CustomUserAdmin)
admin.site.unregister(Group)

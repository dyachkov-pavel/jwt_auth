from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


class UserAdminConfig(UserAdmin):
    readonly_fields = ('refresh_token', 'refresh_token_count')
    list_display = ('id', 'email', 'username', 'first_name', 'last_name',
                    'is_active', 'is_staff', 'is_superuser',
                    'refresh_token', 'refresh_token_count')
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    search_fields = ('username', 'first_name', 'last_name', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'first_name',
                           'last_name', 'email', 'password', 'refresh_token')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username',
                       'first_name', 'last_name',
                       'password1', 'password2',
                       'is_staff', 'is_superuser', 'is_active',),
        }),
    )


admin.site.register(User, UserAdminConfig)

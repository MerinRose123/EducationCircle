from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

class CustomUserAdmin(UserAdmin):
    empty_value_display = '-empty-'
    fieldsets = (
        ('Basic Details', {
            'fields': ('username', 'email', 'first_name', 'last_name', 'password', 'address', 'phone_number')
        }),
        ('Permissions', {
            'fields': (
                'is_superuser', 'is_active', 'is_company_admin', 'is_staff')
        }),

    )

admin.site.register(User, CustomUserAdmin)

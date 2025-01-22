from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """
    Custom admin panel for the CustomUser model.
    """
    model = CustomUser

    # Fields to display in the admin list view
    list_display = ('email', 'user_type', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('user_type', 'is_active', 'is_staff', 'is_superuser')

    # Fieldsets for organizing the admin form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth', 'profile_picture', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Other Info', {'fields': ('user_type', 'is_verified')}),
    )

    # Fields for the "add user" form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type', 'is_active', 'is_staff', 'is_superuser')
        }),
    )

    # Searchable fields
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')

    # Default ordering
    ordering = ('email',)

# Register the CustomUser model with the admin panel
admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import LeasePropertyForm
from .models import CustomUser, Property

class CustomUserAdmin(UserAdmin):
    """
    Custom admin panel for the CustomUser model.
    """
    model = CustomUser

    # Fields to display in the admin list view
    list_display = ('email', 'user_type', 'eth_address', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('user_type', 'is_active', 'is_staff', 'is_superuser')

    # Fieldsets for organizing the admin form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth', 
                       'profile_picture', 'address', 'eth_address')
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Other Info', {'fields': ('user_type', 'is_verified')}),
    )

    # Fields for the "add user" form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type', 'eth_address', 
                       'is_active', 'is_staff', 'is_superuser')
        }),
    )

    # Searchable fields
    search_fields = ('email', 'first_name', 'last_name', 'phone_number', 'eth_address')

    # Default ordering
    ordering = ('email',)

# Register the CustomUser model with the admin panel
admin.site.register(CustomUser, CustomUserAdmin)



class PropertyAdmin(admin.ModelAdmin):
    form = LeasePropertyForm  # Use your custom form in the admin panel
    list_display = ['title', 'location', 'price', 'beds', 'bath', 'garage', 'area', 'date_leased', 'agent']
    search_fields = ['title', 'location', 'price', 'details']
    list_filter = ['location', 'agent', 'price']
    ordering = ['-date_leased']
    
    # Exclude non-editable field from the admin form
    exclude = ('date_leased',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'agent', 'house_image', 'house_video', 'location', 'price', 'details', 'beds', 'bath', 'garage', 'area')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (),  # Remove 'date_leased' from here
        }),
    )

    # Make the non-editable field read-only in the list display
    readonly_fields = ('date_leased',)

admin.site.register(Property, PropertyAdmin)

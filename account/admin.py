from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Unregister the default User admin so we can customize it
admin.site.unregister(User)

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'get_role', 'get_event_name', 'is_staff')
    list_filter = ('is_staff', 'groups')  # Add filters if needed

    # Custom methods to display related fields
    def get_role(self, obj):
        if obj.groups.exists():
            return obj.groups.first().name.split('_')[0]  # Assuming group names are formatted as 'role_event_name'
        return 'No role assigned'

    def get_event_name(self, obj):
        if obj.groups.exists():
            parts = obj.groups.first().name.split('_')
            return parts[1] if len(parts) > 1 else 'No event assigned'
        return 'No event assigned'

    # Renaming columns in the admin view
    get_role.short_description = 'Role'
    get_event_name.short_description = 'Event Name'

# Register the custom admin class for User
admin.site.register(User, CustomUserAdmin)

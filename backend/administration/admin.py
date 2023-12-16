from django.contrib import admin
from .models import Account                
from django.contrib.auth.admin import UserAdmin  

class AccountAdminConfig(UserAdmin):
    """
    Enhanced admin configuration for the Account entity within the admin panel.
    """

    # Defining the fields that can be searched in the admin panel
    search_fields = ('email', 'username', 'fullname', 'profile_id')

    # Uncomment to enable sorting by start_date in a descending order
    ordering = ('-date_joined',)

    # Specifying the fields to be shown in the admin list view
    list_display = ('email', 'username', 'fullname', 'profile_id','is_staff')


# Register the Account model with the custom admin configuration
admin.site.register(Account, AccountAdminConfig)

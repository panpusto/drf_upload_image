from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser, AccountTier


class CustomUserAdmin(UserAdmin):
    """Edits and adds fields for displaying list of users in admin panel."""
    model = CustomUser
    list_display = [
        'email',
        'is_staff',
        'account_tier',
    ]
    fieldsets = UserAdmin.fieldsets + (
        (None,
         {'fields': (
            'account_tier',)
         }),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None,
         {'fields': (
             'account_tier',)
         }),)


class AccountTierAdmin(admin.ModelAdmin):
    """Edits fields for displaying list of available account tiers in admin panel."""
    model = AccountTier
    list_display = [
        'name',
        'admin_thumbnail_sizes',
        'is_expiring_link',
        'is_original_file'
    ]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(AccountTier, AccountTierAdmin)

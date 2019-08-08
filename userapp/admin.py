from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from userapp.models import *

# Register your models here.

######################
######################


class MyUserAdmin(UserAdmin):
    fieldsets = (
            (None, {'fields': ('username', 'password')}),
            (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'usertype', 'email')}),
            (_('Permissions'), {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            }),
            (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        )

    list_display = ('username', 'phone', 'first_name', 'last_name', 'is_staff')

######################
######################


class AddressAdmin(admin.ModelAdmin):
    list_display = ('addr', 'user')
    list_filter = ('user',)
    list_display_links = ('addr',)

######################
######################


admin.site.register(Address, AddressAdmin)
admin.site.register(User, MyUserAdmin)

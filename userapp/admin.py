from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from userapp.models import *
from django.utils.translation import ugettext_lazy as _
# Register your models here.

######################
######################


class AddressAdmin(admin.ModelAdmin):
    list_display = ('addr', 'user')
    list_filter = ('user',)
    list_display_links = ('addr',)

######################
######################


class SmsInlineAdmin(admin.TabularInline):
    model = Sms.users.through
    extra = 0
    fields = ['code', 'created_at']
    readonly_fields = ['code', 'created_at']

    def code(self, instance):
        return instance.sms.code

    def created_at(self, instance):
        return instance.sms.created_at

    code.short_description = 'code'
    created_at.short_description = 'created_at'

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

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
    list_display_links = ('username', 'phone',)
    inlines = UserAdmin.inlines + [SmsInlineAdmin, ]

######################
######################


admin.site.register(Address, AddressAdmin)
admin.site.register(User, MyUserAdmin)
admin.site.register(Sms)

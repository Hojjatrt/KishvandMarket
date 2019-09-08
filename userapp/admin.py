from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from leaflet.admin import LeafletGeoAdmin
from userapp.models import *
from django.utils.translation import ugettext_lazy as _
# Register your models here.

######################
######################


class AddressAdmin(LeafletGeoAdmin):
    list_display = ('name', 'address', 'user')
    list_filter = ('user',)
    list_display_links = ('name', 'address',)

    settings_overrides = {
        'DEFAULT_CENTER': (26.535254, 53.976629),
        'MIN_ZOOM': 10,
        'MAX_ZOOM': 18,
        'SCALE': 'both',
        'SPATIAL_EXTENT': (53.766837, 26.619103, 54.209680, 26.446682),
    }
    def address(self, obj):
        return obj.addr[:25] + '...'

######################
######################


class SmsInlineAdmin(admin.TabularInline):
    model = VerifyCode
    extra = 0
    fields = ['code', 'created_at']
    readonly_fields = ['code', 'created_at']

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
admin.site.register(VerifyCode)
admin.site.register(Massage)

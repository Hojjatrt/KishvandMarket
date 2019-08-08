from django.contrib import admin
from userapp.models import *
# Register your models here.

######################
######################


class AddressAdmin(admin.ModelAdmin):
    list_display = ('addr', 'user')
    list_filter = ('user',)
    list_display_links = ('addr',)


######################
######################

# admin.site.register(Address, AddressAdmin)
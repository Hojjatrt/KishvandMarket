from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Tag)
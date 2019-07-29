from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Product)
admin.site.register(SubCategory)
admin.site.register(MainCategory)
admin.site.register(Tag)
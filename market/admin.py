from django.contrib import admin
from .models import *
from .forms import *
from sorl.thumbnail.admin import AdminImageMixin


# Register your models here.
######################
######################


class ProductImage_inline(AdminImageMixin, admin.TabularInline):
    model = Image
    extra = 0


class ProductSpecies_inline(admin.TabularInline):
    model = ProductSpecie
    extra = 0


class ProductParameters_inline(admin.TabularInline):
    model = ProductParameter
    extra = 0


class ProductStocks_inline(admin.TabularInline):
    model = Stock
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    list_filter = ('status', 'categories')
    list_display_links = ('id', 'name',)
    inlines = (ProductSpecies_inline, ProductParameters_inline, ProductStocks_inline,
               ProductImage_inline)
    form = ProductAdminForm

######################
######################


class StockAdmin(admin.ModelAdmin):
    list_display = ('price', 'qnt', 'discount_ratio')

######################
######################


class ImageAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('get_image', 'prod',)
    list_filter = ('prod',)
    list_display_links = ('get_image', 'prod',)

    def get_image(self, obj):
        return mark_safe('<img src="{url}" width="100" height=100 />'.format(
            url=obj.image.url,)
        )


######################
######################


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'title', 'parent')
    list_filter = ('parent',)
    list_display_links = ('get_image', 'title',)

    def get_image(self, obj):
        return mark_safe('<img src="{url}" width="100" height=100 />'.format(
            url=obj.thumb.url,)
        )

######################
######################


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Stock, StockAdmin)
admin.site.register(Image, ImageAdmin)

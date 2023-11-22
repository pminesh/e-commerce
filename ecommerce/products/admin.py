from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from ecommerce.custom_auth.admin import UserAdmin
from ecommerce.products.models import Product, ProductPhoto


class ProductInline(admin.TabularInline):
    model = ProductPhoto
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price',)
    inlines = (ProductInline,)


# admin.site.register(Product, ProductAdmin)

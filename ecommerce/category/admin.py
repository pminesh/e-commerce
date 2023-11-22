from django.contrib import admin
from ecommerce.category.models import Category


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    readonly_fields = ('slug',)


admin.site.register(Category, CategoryAdmin)

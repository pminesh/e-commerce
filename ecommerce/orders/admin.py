from django.contrib import admin
from ecommerce.orders.models import Order, OrderDetail


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_number', 'total', 'ordered_date', 'payment_type', 'address', 'status']

    inlines = (OrderDetailInline, )


@admin.register(OrderDetail)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'quantity', 'price']
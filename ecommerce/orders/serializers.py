import random

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from unicef_restlib.serializers import UserContextSerializerMixin

from ecommerce.cart.models import Cart
from ecommerce.custom_auth.models import Address
from ecommerce.custom_auth.serializers import AddressSerializer
from ecommerce.orders.models import Order, OrderDetail
from ecommerce.products.models import Product
from ecommerce.products.serializers import ProductSerializer


class OrderDetailSerializer(UserContextSerializerMixin, serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = OrderDetail
        fields = ('product', 'quantity', 'price', 'order','product_details')
        read_only_fields = ('order', 'product', 'quantity', 'price')


class OrderSerializer(UserContextSerializerMixin, serializers.ModelSerializer):
    address_detail = AddressSerializer(source='address', read_only=True)
    # product_detail = serializers.SerializerMethodField()
    customer_order = OrderDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ('id', 'order_number', 'total', 'ordered_date', 'payment_type', 'status', 'user', 'address', 'address_detail', 'customer_order')
        read_only_fields = ('user', 'payment_type', 'order_number')

    def validate(self, attrs):
        address = Address.objects.filter(id=attrs['address'].id, user=self.context['request'].user)
        if not address:
            raise ValidationError('Enter valid address')
        return super().validate(attrs)

    def create(self, validated_data):
        user = self.get_user()
        order_number = random.randint(10000, 99999)
        carts = Cart.objects.filter(user=user)

        if not carts:
            raise ValidationError('Your cart is empty')

        validated_data['order_number'] = order_number
        validated_data['user'] = user
        validated_data['payment_type'] = 'Cash'

        data = super().create(validated_data)

        for cart in carts:
            data.total += cart.product.price * cart.quantity

            # OrderDetail.objects.create(order=data, product=cart.product, quantity=cart.quantity,
            #                            price=cart.product.price)

            OrderDetail.objects.bulk_create(
                [
                OrderDetail(order=data, product=cart.product, quantity=cart.quantity,
                                       price=cart.product.price)
                ]
            )
        data.save()
        carts.delete()
        return data

    # def get_product_detail(self, obj):
    #     print(obj)
    #     return OrderDetailSerializer(obj.customer_order.all(), many=True).data

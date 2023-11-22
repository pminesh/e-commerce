# from django.contrib.gis.gdal.raster import source
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from unicef_restlib.serializers import UserContextSerializerMixin

from ecommerce.cart.models import Cart
from ecommerce.products.models import Product
from ecommerce.products.serializers import ProductSerializer


class CartSerializer(UserContextSerializerMixin, serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'product', 'quantity', 'product_details')
        read_only_fields = ('user',)

    def create(self, validated_data):
        user = self.get_user()
        product = Cart.objects.filter(product=validated_data['product'], user=user)
        if product:
            raise ValidationError('cart already added')

        validated_data['user'] = user
        return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     instance['quantity'] = validated_data['quantity']
    #     instance.save()
    #     return super().update(instance,validated_data)

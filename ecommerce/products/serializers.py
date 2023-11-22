
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from unicef_restlib.serializers import UserContextSerializerMixin


from ecommerce.category.serializer import CategorySerializer
from ecommerce.custom_auth.serializers import BaseUserSerializer
from ecommerce.products.models import Product, ProductPhoto


class ProductPhotoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProductPhoto
        fields = ('id', 'image', 'width', 'height',)
        extra_kwargs = {
            'image': {'required': True, "allow_null": False}
        }

    def create(self, validated_data):
        validated_data['product_id'] = self.context['view'].kwargs.get('nested_1_pk')
        if self.context['view'].kwargs.get('nested_1_slug'):
            product_id = Product.objects.get(slug=self.context['view'].kwargs.get('nested_1_slug'))
            validated_data['product_id'] = product_id.id
        return super().create(validated_data)


class ProductSerializer(UserContextSerializerMixin, serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)
    photo = serializers.SerializerMethodField()
    category_details = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'category', 'category_details', 'name', 'price', 'discount', 'slug', 'description', 'stocks', 'photo', 'user')
        extra_kwargs = {
            'category': {'required': True},
            'name': {'required': True},
            'price': {'required': True}
        }
        read_only_fields = ('slug',)

        validators = [UniqueTogetherValidator(queryset=Product.objects.all(), fields=('name',))]

    # def validate(self, attrs):
    #     try:
    #         product = Product.objects.get(name=attrs['name'])
    #         if product:
    #             raise ValidationError('Product name is already exists!!')
    #     except Product.DoesNotExist:
    #         return super().validate(attrs)
    #     except KeyError:
    #         return super().validate(attrs)

    def create(self, validate_data):
        user = self.get_user()
        validate_data['user'] = user
        return super().create(validate_data)

    # def update(self, instance, validated_data):
    #     if 'name' in validated_data:
    #         raise ValidationError("You can't update product name")
    #     return super().update(instance, validated_data)

    def get_photo(self, obj):
        return ProductPhotoSerializer(obj.product_images.all(), many=True).data



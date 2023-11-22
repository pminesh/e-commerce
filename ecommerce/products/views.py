from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from ecommerce.products.models import Product,ProductPhoto
from ecommerce.products.permissions import IsSeller, IsProduct
from ecommerce.products.serializers import ProductSerializer, ProductPhotoSerializer
from rest_framework.permissions import AllowAny

from ecommerce.utils.permissions import IsReadAction


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsReadAction | IsSeller, IsProduct]
    lookup_field = 'slug'

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name', 'price', )

class PhotoViewSet(ModelViewSet):
    queryset = ProductPhoto.objects.all()
    serializer_class = ProductPhotoSerializer
    related_model = Product
    permission_classes = [IsAuthenticated, IsReadAction | IsSeller, IsProduct]

    def get_queryset(self):
        query_set = super().get_queryset()
        # print("photo = ",self.get_object())
        # return query_set.filter(product=self.get_object())
        return query_set


    # @action(methods=['post'], url_path='product-image/create', url_name='product_image_create',
    #         detail=True)
    # def set_product_photo(self, request, *args, **kwargs):
    #     product = self.get_object()
    #
    #     serializer = ProductPhotoSerializer(data=request.data)
    #     if not serializer.is_valid():
    #         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    #
    #     data = serializer.validated_data
    #     data.update({'product': product})
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    # @action(methods=['delete'], url_path='product-image/delete/(?P<photo_id>[0-9]+)', url_name='product_image_delete',
    #         detail=True)
    # def delete_image(self, request, *args, **kwargs):
    #     get_object_or_404(ProductPhoto, pk=self.kwargs.get('photo_id')).delete()
    #     return Response({"success": "Photo deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    #
    # @action(methods=['patch'], url_path='product-image/update/(?P<photo_id>[0-9]+)', url_name="product_image_update",
    #         detail=True)
    # def update_photo(self, request, *args, **kwargs):
    #     product = self.get_object()
    #     print("product = ", product)
    #     photo_id = get_object_or_404(ProductPhoto, pk=self.kwargs.get('photo_id')).delete()

        # serializer = ProductPhotoSerializer(data=request.data)
        # if not serializer.is_valid():
        #     return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        #
        # data = serializer.validated_data
        # data.update({'pk': product.id, 'product': product})
        # serializer.save()
        # return Response(serializer.data, status=status.HTTP_201_CREATED)



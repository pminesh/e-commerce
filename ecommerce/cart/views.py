from django.db import models
from django.db.models import F, Sum
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ecommerce.cart.models import Cart
from ecommerce.cart.permissions import IsUser, IsSelf
from ecommerce.cart.serializers import CartSerializer
from ecommerce.products.permissions import IsSeller


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    # permission_classes = [IsAuthenticated, IsUser, IsSelf, ~IsSeller]
    permission_classes = [IsAuthenticated, IsUser, IsSelf]

    # filter_backends = (DjangoFilterBackend, OrderingFilter)



    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(user=self.request.user)

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data.update(self.filter_queryset(self.get_queryset()).aggregate(
            total=Sum(F('quantity') * F('product__price'), output_field=models.FloatField())))
        return response
from django.db import models
from django.db.models import Count, F
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ecommerce.cart.models import Cart
from ecommerce.cart.permissions import IsUser, IsSelf
from ecommerce.orders.models import Order, OrderDetail
from ecommerce.orders.serializers import OrderSerializer,OrderDetailSerializer
from ecommerce.products.permissions import IsSeller


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsSelf, IsUser]

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(user=self.request.user)

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data.update(self.filter_queryset(self.get_queryset()).aggregate(
            total=Count(('id'))))
        return response

# class OrderDetailsViewSet(viewsets.ModelViewSet):
#     queryset = OrderDetail.objects.all()
#     serializer_class = OrderDetailSerializer
#     permission_classes = [IsAuthenticated, IsUser, IsSelf]
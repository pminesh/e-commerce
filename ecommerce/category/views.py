from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from ecommerce.category.models import Category
from ecommerce.category.serializer import CategorySerializer
from ecommerce.utils.permissions import IsReadAction


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    permission_classes = [IsReadAction]

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name', 'slug',)
    ordering_fields = ('name',)
    # ordering = '-id'
    filterset_fields = ('slug',)

    def get_queryset(self):
        search = self.request.query_params.get('search')
        if search:
            return Category.objects.filter(slug__iexact=search)
        return super().get_queryset()
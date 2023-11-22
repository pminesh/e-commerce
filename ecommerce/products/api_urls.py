from django.urls import path, include
from rest_framework import routers
from unicef_restlib.routers import NestedComplexRouter

from ecommerce.products import views

router = routers.SimpleRouter()


router.register('product', views.ProductViewSet, basename='product')
product_router = NestedComplexRouter(router, r'product')
product_router.register(r'photos', views.PhotoViewSet, basename='product-photos')

app_name = 'product'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
]

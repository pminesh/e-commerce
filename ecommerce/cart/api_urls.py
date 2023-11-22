from django.urls import path, include

from rest_framework import routers

from ecommerce.cart import views

router = routers.SimpleRouter()

router.register('cart', views.CartViewSet, basename='Cart')

app_name = 'cart'
urlpatterns = [
    path('', include(router.urls)),
]
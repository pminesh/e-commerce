from django.urls import path, include
from rest_framework import routers
from ecommerce.custom_auth import views

router = routers.SimpleRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('auth', views.UserAuthViewSet, basename='auth')
router.register('address', views.AddressViewSet, basename='address')

app_name = 'custom-auth'

urlpatterns = [
    path('', include(router.urls)),
]
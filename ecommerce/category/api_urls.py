from django.urls import path, include
from rest_framework import routers
from ecommerce.category import views

router = routers.SimpleRouter()
router.register('category', views.CategoryViewSet, basename='category')

app_name = 'category'

urlpatterns = [
    path('', include(router.urls)),
]


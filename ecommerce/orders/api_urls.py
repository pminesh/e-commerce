from django.urls import path, include
from rest_framework import routers

from ecommerce.orders import views
router = routers.SimpleRouter()

router.register('order', views.OrderViewSet, basename='order')
# router.register('placeorder', views.OrderDetailsViewSet, basename='orderDetails')

app_name = 'orders'

urlpatterns = [
    path('', include(router.urls)),
]

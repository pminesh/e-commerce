from django.urls import include, path
from rest_framework.routers import SimpleRouter

from ecommerce.registrations.views import RegistrationViewSet

router = SimpleRouter()

router.register('',RegistrationViewSet, basename='registration')

app_name = 'registration'

urlpatterns = [
    path('', include(router.urls)),
]
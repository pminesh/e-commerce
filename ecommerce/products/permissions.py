from rest_framework import permissions

from ecommerce.custom_auth.models import ApplicationUser


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == ApplicationUser.USER_TYPES.seller


class IsProduct(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

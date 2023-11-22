from rest_framework.permissions import BasePermission

from ecommerce.custom_auth.models import ApplicationUser


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == ApplicationUser.USER_TYPES.users


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

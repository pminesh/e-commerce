from rest_framework import permissions


class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print("obj = ", obj)
        print("request = ", request.user)
        return obj == request.user


class IsAddressCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


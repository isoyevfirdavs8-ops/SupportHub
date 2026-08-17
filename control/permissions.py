from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):


    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False


        if request.method in permissions.SAFE_METHODS:
            return True


        return request.user.role == 'admin' or request.user.is_staff


from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):


    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsOperator(BasePermission):


    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "operator"
        )


class IsTicketOwner(BasePermission):


    def has_object_permission(self, request, view, obj):
        return obj.client == request.user


class IsAdminOrAssignedOperator(BasePermission):


    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "operator":
            return obj.operator == request.user

        return False
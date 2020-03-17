from rest_framework.permissions import BasePermission


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, user):  # single obj 접근 권한
        return user == request.user
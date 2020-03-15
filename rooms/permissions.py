from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    # drf 문서 custom permissions

    def has_object_permission(self, request, view, room):  # obj_pm 이어야! obj 받아야 하므로
        return room.user == request.user

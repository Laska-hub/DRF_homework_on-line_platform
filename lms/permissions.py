from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Пользователь состоит в группе moderators
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(
                name="moderators"
            ).exists()
        )


class IsOwner(BasePermission):
    """
    Пользователь является владельцем объекта
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and obj.owner == request.user
        )


class IsOwnerOrModerator(BasePermission):
    """
    Владелец объекта или модератор
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (
                obj.owner == request.user
                or request.user.groups.filter(
                    name="moderators"
                ).exists()
            )
        )


class IsNotModerator(BasePermission):
    """
    Пользователь НЕ состоит в группе moderators
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and not request.user.groups.filter(
                name="moderators"
            ).exists()
        )

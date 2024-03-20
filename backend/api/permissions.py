from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Органичения прав.
    Доступ на чтение у всех пользователей, в том числе у анонимных.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin
        )


class IsAuthorOrReadOnly(BasePermission):
    """
    Органичения прав.
    Доступ на чтение у всех пользователей, в том числе у анонимных.
    Доступ на изменение объекта есть только у автора.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsStaffOwnerOrReadOnly(BasePermission):
    '''Пермишен, проверяющий, есть ли у пользователя права модератора или выше,
    либо авторство объекта
    '''

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS or request.user.is_moderator
                or request.user.is_admin or request.user == obj.author)


class IsAdminOrReadOnly(BasePermission):
    '''Пермишен, проверяющий, есть ли у пользователя права админа или выше.

    Разрешает 'GET', 'HEAD', 'OPTIONS' методы.
    '''

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_admin)


class IsAdmin(BasePermission):
    "Пермишен, проверяющий, есть ли у пользователя права админа или выше."

    def has_permission(self, request, view):
        return request.user.is_admin

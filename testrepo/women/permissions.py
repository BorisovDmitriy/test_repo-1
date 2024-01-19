from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # проверяем запрос на безопасность это должен быть запрос GET,HEAD,OPTIONS только на чтение а не на изменение
            return True

        return bool(request.user and request.user.is_staff) # скопировал строку из BasePermission
        # если нет только для admina методы изменения POST DELETE PUCH итд

class IsOwnerOrReadOnly(permissions.BasePermission):
   def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user



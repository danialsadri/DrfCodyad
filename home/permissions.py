from rest_framework.permissions import BasePermission
from .models import BlockUser


class BlockListPermission(BasePermission):
    def has_permission(self, request, view):
        blocked = BlockUser.objects.filter(username=request.user.username).exists()
        return not blocked

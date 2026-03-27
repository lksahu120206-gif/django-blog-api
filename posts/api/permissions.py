from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied


class IsAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Allows GET/HEAD/OPTIONS for anyone, 
    modify/delete only for post/comment author.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in self.safe_methods:
            return True
        return obj.author == request.user


class IsCommentAuthorOrReadOnly(IsAuthorOrReadOnly):
    """
    Permission for comments.
    """
    pass


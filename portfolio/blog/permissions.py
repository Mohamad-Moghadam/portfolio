from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAuthorOrSuperuser(IsAuthenticated):
    """
    Permission class to check if the user is authenticated and 
    either the author of the blog or a superuser.
    """
    def has_object_permission(self, request, view, obj):
        # For views that operate on objects (Retrieve, Update, Destroy)
        # First check if authenticated (via IsAuthenticated parent)
        # Then check if superuser or author
        return request.user.is_superuser or obj.author == request.user
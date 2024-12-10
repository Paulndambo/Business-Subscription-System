from rest_framework.permissions import BasePermission


class IsBusinessOwner(BasePermission):
    """
    Custom permission to allow only users with the role 'Business Owner' to perform POST requests.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Allow GET requests for all authenticated users
        if request.method == "GET":
            return True

        # Allow POST requests only for users with role 'Business Owner'
        return request.user.role == "Business Owner"

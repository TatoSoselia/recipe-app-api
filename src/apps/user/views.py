"""
Views for the user API.
"""
from rest_framework import permissions
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
)
from apps.user.serializers import UserSerializer


class CreateUserView(CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class ManageUserView(RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user."""
        return self.request.user

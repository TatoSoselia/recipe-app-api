"""
Views for the user API.
"""
from rest_framework.generics import (
    CreateAPIView
)
from apps.user.serializers import UserSerializer


class CreateUserView(CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer

"""
Views for the recipe APIs.
"""
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from apps.recipe.models import Recipe, Tag
from apps.recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
    TagSerializer,
)


class RecipeViewSet(viewsets.ModelViewSet):
    """ View for managing recipes APIs."""
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return (self.queryset.filter(user=self.request.user)
                .select_related().order_by('-id'))

    def get_serializer_class(self):
        """Return appropriate serializer class for request."""
        if self.action == 'list':
            return RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Manage tags in the database."""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve tags for the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

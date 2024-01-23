"""
Views for the recipe APIs.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.recipe.models import Recipe
from apps.recipe.serializers import RecipeSerializer, RecipeDetailSerializer


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

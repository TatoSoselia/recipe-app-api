"""
Views for the recipe APIs.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.base.views import BaseRecipeAttrViewSet

from apps.recipe.models import Recipe, Tag, Ingredient
from apps.recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
    TagSerializer, IngredientSerializer,
    RecipeImageSerializer,
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
        elif self.action == 'upload_image':
            return RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve tags for the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve ingredients for the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

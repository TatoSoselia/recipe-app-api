"""base views"""
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated


class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base views for recipe attributes."""

    permission_classes = [IsAuthenticated]

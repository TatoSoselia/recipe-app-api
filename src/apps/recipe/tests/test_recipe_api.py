"""
Tests for the Recipe API.
"""
from django.test import TestCase
from django.urls import reverse

from apps.recipe.models import Recipe
from apps.user.factories import UserFactory
from apps.recipe.factories import RecipeFactory
from apps.recipe.serializers import RecipeSerializer

from rest_framework import status
from rest_framework.test import APIClient

RECIPE_URL = reverse('recipe:recipe-list')


class PublicRecipeApiTests(TestCase):
    """Test the publicly available recipe functionality."""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that login is required for retrieving recipe details."""
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """Test the recipe functionality for authenticated users."""
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory.create()
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        RecipeFactory.create_batch(3, user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test retrieving recipes is limited for authenticated user."""
        other_user = UserFactory.create()
        RecipeFactory.create_batch(3, user=other_user)
        RecipeFactory.create_batch(3, user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user).order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

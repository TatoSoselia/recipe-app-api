"""
Tests for the Recipe API.
"""
from django.test import TestCase
from django.urls import reverse

from apps.recipe.models import Recipe
from apps.user.factories import UserFactory
from apps.recipe.factories import RecipeFactory
from apps.recipe.serializers import RecipeSerializer, RecipeDetailSerializer

from rest_framework import status
from rest_framework.test import APIClient

import decimal

RECIPE_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Create and return a recipe detail URL."""
    return reverse('recipe:recipe-detail', args=[recipe_id])


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

    def test_get_recipe_detail(self):
        """Test get recipe detail."""
        recipe = RecipeFactory.create_batch(1, user=self.user)[0]

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a new recipe."""
        payload = {
            "title": "Test Recipe",
            "time_minutes": 30,
            "price": decimal.Decimal("5.99")
        }

        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for kay, value in payload.items():
            self.assertEqual(getattr(recipe, kay), value)
        self.assertEqual(recipe.user, self.user)

"""
Tests for the ingredients API.
"""
from apps.recipe.factories import UserFactory, IngredientFactory
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from apps.recipe.models import Ingredient
from apps.recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')


def detail_url(ingredient_id):
    """Create and return an ingredient detail URL."""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


class PublicIngredientApiTests(TestCase):
    """Test the publicly available ingredients API"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that login is required for retrieving ingredients"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTests(TestCase):
    """Test the ingredients API for authenticated user"""
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(self.user)

    def test_retrive_ingredients(self):
        """Test retrieving ingredients"""
        IngredientFactory.create_batch(3, user=self.user)

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test retrieving ingredients is limited to user"""
        other_user = UserFactory.create()

        IngredientFactory.create_batch(3, user=other_user)
        IngredientFactory.create_batch(2, user=self.user)
        ingredients = (Ingredient.objects.filter(user=self.user)
                       .order_by('-name'))

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        for i in range(len(ingredients)):
            self.assertEqual(ingredients[i].name, res.data[i]['name'])
            self.assertEqual(ingredients[i].id, res.data[i]['id'])

    def test_update_ingredient_successful(self):
        """Test updating an ingredient"""
        ingredient = IngredientFactory.create(user=self.user, name='name')

        payload = {'name': 'updated name'}
        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, res.data['name'])

    def test_delete_ingredient_successful(self):
        """Test deleting an ingredient"""
        ingredient = IngredientFactory.create(user=self.user, name='name')

        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredient = Ingredient.objects.filter(id=ingredient.id)
        self.assertFalse(ingredient.exists())

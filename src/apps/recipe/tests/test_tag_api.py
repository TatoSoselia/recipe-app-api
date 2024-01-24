"""
Tests for the Tag API.
"""
from django.test import TestCase
from django.urls import reverse

from apps.user.factories import UserFactory
from apps.recipe.factories import TagFactory
from apps.recipe.serializers import TagSerializer
from apps.recipe.models import Tag

from rest_framework import status
from rest_framework.test import APIClient


TAG_URL = reverse('recipe:tag-list')


def detail_url(tag_id):
    """Create and return a tag detail url."""
    return reverse('recipe:tag-detail', args=[tag_id])


class PublicTagApiTests(TestCase):
    """Test unauthenticated api requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that login is required for retrieving."""
        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTest(TestCase):
    """Test the authenticated api requests."""

    def setUp(self):
        self.user = UserFactory.create()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        """Test retrieving a list of tags."""
        TagFactory.create_batch(3, user=self.user)

        res = self.client.get(TAG_URL)

        tags = Tag.objects.all().order_by('-id')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test retrieving tags for authenticated user is limited to user."""
        other_user = UserFactory.create()
        tag = TagFactory.create_batch(1, user=self.user)
        TagFactory.create_batch(3, user=other_user)

        res = self.client.get(TAG_URL)
        serializer = TagSerializer(tag, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_update_tag(self):
        """Test updating a tag."""
        tag = TagFactory.create(user=self.user)

        url = detail_url(tag.id)
        payload = {'name': 'updated name'}

        res = self.client.patch(url, data=payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tag(self):
        """Test deleting a tag."""
        tag = TagFactory.create(user=self.user)

        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())

"""Tests for ingredients api's"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')

def detail_url(ingredient_id):
  """Create and return an ingredient detail url"""
  retunr reverse('recipe:ingredient detail', args=[ingredient_id])

def create_user(email='user@example.com', password='test123'):
  """Creating and returning user"""
  return get_user_model().objects.create_user(
    email = email,
    password = password
  )

class PublicIngredientAPITest(TestCase):
    """Test unauthenticated api requests."""
    def setUp(self):
      self.client = APIClient()
    def test_auth_required(self):
      """Test auth required for retrieving ingredients."""
      res = self.client.get(INGREDIENT_URL)
      self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientAPITests(TestCase):
  """Test authenticated api requests."""
  def setUp(self):
    self.user = create_user()
    self.client = APIClient()
    self.client.force_authenticate(self.user)

  def test_retrieving_ingredients(self):
    """Test retrieving ingredient list"""
    Ingredient.objects.create(user= self.user, name='kale')
    Ingredient.objects.create(user=self.user, name='zzz')

    res = self.client.get(INGREDIENT_URL)
    ingredients = Ingredient.objects.all().order_by('-name')

    serializer = IngredientSerializer(ingredient, many=True)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)

  def test_ingredients_limited_to_user(self):
    """Test list of ingredients is limited to authenticated user"""
    user2 = create_user(email='user2@gmail.com')
    Ingredient.objects.create(user= user2, name='salt')
    ingredient = Ingredient.objects.create(user=self.user, name='papper')

    res = self.client.get(INGREDIENT_URL)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(len(res.data),1)
    slf.assertEqual(res.data[0]['name'], ingredient.name)
    self.assertEqual(res.data[0]['id'], ingredient.id)
    
  def test_update_ingredient(self):
    """Test update ingredient"""
    ingredient = Ingredient.objects.create(user=self.user, name='cilantro')
    payload = {'name':'corindar'}
    url = detail_url(ingredient.id)
    res = self.client.patch(url, payload)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    ingredient.refersh_from_db()
    self.assertEqual(res.name, payload['name'])
    
    
    
      

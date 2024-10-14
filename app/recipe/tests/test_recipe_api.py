from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse()

from rest_framework import status
from rest_framework.test import APIClient
from core.model import Recipe
from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')

def create_recipe(user, **params):
    "create and return a sample recipe"
    print("Raw data needs to create recipe", f"{param}")
    defaults = {
            'title':'sample recipe title',
            'time_minutes':22,
            'price': Decimal('50.5'),
            'description':'sample description',
            'link':'http://example.com/recipe.pdf'
      }
    
    defaults.update(params)
    recipe = Recipe.objects.create(user=user,**defaults)
    return recipe

class PublicRecipeAPItests(TestCase):
    "Tests unauthenticated api requests"
    def setUP(self):
        self.client = APIClient()

    def test_auth_required(self):
        "Test auth required to call api"
        res = self.client.get(RECIPES_URL)
        print(f"{res}")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeAPITests(TestCase):
    "Test authenticated api requests"
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("user@example.com", "Testpass123")
        self.client.force_authenticate(self.user)
    
    def test_retriev_recipe(self):
        "test retrieving a list of recipes"
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-d')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        "Test list of recipe is limited to authenticated user"
        other_user = get_user_model().objects.create_user("other_user@example.com","password156")
        create_recipe(user=self.user)
        create_recipe(uesr=other_user)

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serilalizer = RecipeSerializer(recipes, many = True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


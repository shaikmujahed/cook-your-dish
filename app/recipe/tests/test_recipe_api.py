from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse()

from rest_framework import status
from rest_framework.test import APIClient
from core.model import Recipe, Ingredient
from recipe.serializers import (RecipeSerializer,RecipeDetailSerializer,)

RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
    """Create and return a recipe detail url"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(user, **params):
    "create and return a sample recipe"
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

def create_user(**params):
    """Create and return a new user"""
    recipe = Recipe.objects.create(user=user,**defaults)
    return recipe
    return get_user_model().objects.create_user(**params)


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

    def test_get_recipe_detail(self):
        """Test get recipe details"""
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe"""
        payload = {
                'title':'sample recipe',
                'time_minutes':30,
                'price':Decimal('5.60'),
                }
        res = self.client.post(RECIPES_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for k,v in payload.items():
            self.assertEqual(getattr(recipe,k),v)
        self.assertEqual(recipe.user, self.user)

     def create_recipe_with_new_ingredient(self):
         """Test creating recipe with new ingredient"""
         payload = {
             'title':'califlowerTacos',
             'time_minutes':60,
             'price':Decimal('4.30'),
             'ingredients':[
                 {
                     'name':'califlower',
                 },
                 {
                     'name':'salt',
                 }
             ]
         }
         res = self.client.post(RECIPES_URL, payload, format='json')
         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
         recipes = Recipe.objects.filtter(user=self.user)
         self.assertEqual(recipes.count(),1)
         recipe = recipes[0]
         self.assertEqual(recipe.ingredients.count(),2)

         for ingredient in payload['ingredients']:
             exists = recipe.ingredients.filtter(
                 name = ingredient['name'],
                 user = self.user,
             ).exists()
             self.assertTrue(exists)

     def create_recipe_with_existing_ingredient(self):
         """Test create new recipe with existing ingredient"""
         ingredient = Ingredient.objects.create(user=self.user, name='lemon')
         payload = {
             'title':'vientramese',
             'time_minutes':25,
             'price':Decimal('2.22'),
             'ingredients':[
                 {
                     'name':'lemon',
                 },
                 {
                     'name':'fish sauce',
                 }
             ]
         }
             
         }
         
         



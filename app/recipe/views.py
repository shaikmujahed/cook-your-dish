#Views for the recipe APIs

from rest_framework import (
viewsets,
mixins,
status
)
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Ingredient
from recipe import serializers

class RecipeViewset(viewsets.ModelViewset):
    """View for manage recipe APIs"""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        """Retriev recipes for authenticated users"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.RecipeSerializer
        return serializer_class

class IngredientViewset(mixins.ListModelMixin, mixins.UpdateModelMixin,viewsets.GenericViewset):
    """Manage ingredient in database"""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """filter queryset to authenticate user"""
        return self.queryset.filtter(user=self.request.user).order_by('-name')




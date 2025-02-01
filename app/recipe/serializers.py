"""Serializers for recipe APIs"""

from rest_framework import serializers
from core.models import Recipe, Ingredient


class RecipeSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ["id","title","time_minutes","price","link"]
        read_only_fields =["id"]

class RecipeDetailserializer(RecipeSerializer):
    """Serializer for recipe detail view"""
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]

class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient"""
    class Meta:
        model = Ingredient
        fields = ['id','name']
        read_only_fields = ['id']
        

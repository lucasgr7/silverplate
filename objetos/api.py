from rest_framework import serializers
from .models import Ingredient, IngredientNickname, Recipe, RecipeIngredient, RecipeStep
from django.contrib.auth.models import User

class IngredientApi(serializers.HyperlinkedModelSerializer):
    nicknames = serializers.StringRelatedField(many=True)
    class Meta:
        model = Ingredient
        fields = ('id', 'description','image', 'nicknames')

class UserApi(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class RecipeIngredientApi(serializers.HyperlinkedModelSerializer):
    ingredient = IngredientApi(many=False, read_only=True)
    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'description')

class RecipeStepApi(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecipeStep
        fields = ('step')

class RecipeApi(serializers.HyperlinkedModelSerializer):
    creator = UserApi(many=False, read_only=True)
    ingredients = RecipeIngredientApi(many=True, read_only=True)
    steps = serializers.StringRelatedField(many=True)
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'creator', 'ingredients', 'steps', 'description', 'language')
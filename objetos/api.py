from rest_framework import serializers
from .models import Ingredient, IngredientNickname

class IngredientApi(serializers.HyperlinkedModelSerializer):
    nicknames = serializers.StringRelatedField(many=True)
    class Meta:
        model = Ingredient
        fields = ('id', 'description','image', 'nicknames')
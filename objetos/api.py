from rest_framework import serializers
from .models import Ingredient

class IngredientApi(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'description','image')
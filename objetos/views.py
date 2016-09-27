from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Ingredient
from .api import IngredientApi

# Create your views here.

@api_view(['GET',])
def list_ingredient(request):
    ingredients = Ingredient.objects.all()
    if request.GET.get('description') != '' and request.GET.get('description') != None:
    	ingredients = ingredients.filter(description__icontains=request.GET.get('description'))
    Ingredientapi = IngredientApi(ingredients, many=True)
    # print usuarioApi
    return Response(Ingredientapi.data)
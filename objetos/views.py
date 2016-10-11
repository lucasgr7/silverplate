from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Ingredient, IngredientNickname
from .api import IngredientApi
import json

# Create your views here.

@api_view(['GET',])
def list_ingredient(request):
    ingredients = Ingredient.objects.all()
    if request.GET.get('q') != '' and request.GET.get('q') != None:
    	ingredients = ingredients.filter(description__icontains=request.GET.get('q'))
    api_return = IngredientApi(ingredients, many=True)
    # print usuarioApi
    return Response(api_return.data)

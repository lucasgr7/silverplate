from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Ingredient, IngredientNickname, Recipe
from .api import IngredientApi, RecipeApi
import json

@api_view(['GET',])
def list_recipe(request):
	if not request.GET.get('q'):
		if not request.GET.get('id'):
			recipes = Recipe.objects.filter(id=request.GET.get('id'))
		else:
			recipes = Recipe.objects.all()
	else:
		recipes = Recipe.objects.filter(description__icontains=request.GET.get('q'))
	api_return = RecipeApi(recipes, many=True)
	# print usuarioApi
	print(api_return)
	return Response(api_return.data)
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Ingredient, IngredientNickname, Recipe
from .api import IngredientApi, RecipeApi
import json

# Create your views here.

@api_view(['GET',])
def list_ingredient(request):
	if request.GET.get('q') != '' and request.GET.get('q') != None:
		ingredients = Ingredient.objects.filter(description__icontains=request.GET.get('q'))
	else:
		ingredients = Ingredient.objects.all()
	api_return = IngredientApi(ingredients, many=True)
	# print usuarioApi
	return Response(api_return.data)


@api_view(['GET',])
def list_recipe(request):
	if request.GET.get('q') != '' and request.GET.get('q') != None:
		recipes = Recipe.objects.filter(description__icontains=request.GET.get('q'))
	else:
		recipes = Recipe.objects.all()
	api_return = RecipeApi(recipes, many=True)
	# print usuarioApi
	print(api_return)
	return Response(api_return.data)

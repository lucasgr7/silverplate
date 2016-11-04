from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Ingredient, IngredientNickname, Recipe, RecipeImage, RecipeStep, RecipeIngredient
from .api import IngredientApi, RecipeApi
from django.contrib.auth.models import User

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


@api_view(['POST',])
def save_recipe(request):
	data = []
	if not request.data.get('title'):
		data.append({"error" : "Title may not be blank."})
	if not request.data.get('creator_id'):
		data.append({"error" : "creator may not be blank."})
	if not request.data.get('description'):
		data.append({"error" : "description may not be blank."})
	if not request.data.get('language'):
		data.append({"error" : "language may not be blank."})
	if not request.data.get('steps'):
		data.append({"error" : "you must inform the steps of the reipce."})
	if not request.data.get('ingredients'):
		data.append({"error" : "you must inform the ingredients of the reipce."})
	
	if len(data) > 0:
		return Response(data, status=400)

	try:
		creator = User.objects.get(pk=request.data.get('creator_id'))
	except:
		return Response({"error":"Creator not found or not exist!"}, status=404)

	recipe = Recipe(title=request.data.get('title'),
		creator=creator,
		description=request.data.get('description'),
		language=request.data.get('language'))

	recipe.save()

	if request.data.get('images'):
		for image in request.data.get('images'):
			img = RecipeImage(description=image["description"],
				url=image["url"],
				recipe=recipe)
			img.save()

	step_count = 0
	for step in request.data.get('steps'):
		order = 0
		if not step["order"]:
			order = step_count
		else:
			order = step["order"]
		stp = RecipeStep(step=step["step"],
			order=order,
			recipe=recipe)
		stp.save()


	for ingredient in request.data.get('ingredients'):
		try:
			if not ingredient["description"]:
				return Response({"error":"Ingrdient %s has no description in how to use!" % ingredient['ingredient_id']}, status=500)
		except:
			return Response({"error":"Ingrdient %s miss the attribut description!" % ingredient['ingredient_id']}, status=500)
		
		try:
			model = Ingredient.objects.get(pk=ingredient['ingredient_id'])
		except:
			return Response({"error":"Ingrdient %s not found or not exist!" % ingredient['ingredient_id']}, status=404)

		ing = RecipeIngredient(description=ingredient["description"],
			ingredient=model,
			recipe=recipe)
		ing.save()

	return Response(status=200)
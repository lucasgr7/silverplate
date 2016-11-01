from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Ingredient, IngredientNickname, Recipe
from .api import IngredientApi, RecipeApi
import json

# Create your views here.

@api_view(['GET',])
def list_ingredient(request):
	if not request.GET.get('q'):
		if not request.GET.get('id'):
			ingredients = Ingredient.objects.all()
		else:
			ingredients = Ingredient.objects.filter(id=request.GET.get('id'))
	else:
		ingredients = Ingredient.objects.filter(description__icontains=request.GET.get('q'))
	api_return = IngredientApi(ingredients, many=True)
	# print usuarioApi
	return Response(api_return.data)



@api_view(['POST',])
def save_ingredient(request):
	data = []
	if not request.data.get('description'):
		data.append({"description" : "This field may not be blank."})

	if not request.data.get('image'):
		data.append({"image" : "This field may not be blank."})

	if len(data) > 0:
		return Response(data, status=400)
	else:
		ingredient = Ingredient(
			description=request.data.get('description'),
			image=request.data.get('image'))
		ingredient.save()

	if request.data.get('nicknames') != None and len(request.data.get('nicknames')) > 0:
		for nickname in request.data.get('nicknames'):
			nick = IngredientNickname(ingredient=ingredient,
				nickname=nickname)
			nick.save()
	
	return Response(status=200)

@api_view(['DELETE',])
def delete_ingredient(request):
	if not request.GET.get('id'):
		return Response({"return","Id can't be null"}, status=400)
	else:
		try:
			ingredient = Ingredient.objects.get(pk=request.GET.get('id'))
		except:
			return Response({"return":"Object does not exists"}, status=404)
		ingredient.delete()
		return Response(status=200)

@api_view(['PUT',])
def update_ingredient(request):
	data = []
	if not request.data.get('id'):
		data.append({"error":"Field id must not be blank"})
	if not request.data.get('description'):
		data.append({"error" : "Field description may not be blank."})

	if not request.data.get('image'):
		data.append({"error" : "Field image may not be blank."})

	if len(data) > 0:
		return Response(data, status=400)
	else:
		try:
			ingredient = Ingredient(
				id=request.data.get('id'),
				description=request.data.get('description'),
				image=request.data.get('image'))

			ingredient.save()
		except:
			return Response({'error':'error trying to save the changes'}, status=400)

	delete_nicknames = IngredientNickname.objects.filter(ingredient_id=ingredient.id)
	for nickname_saved in delete_nicknames:
		nickname_saved.delete()
			
	if request.data.get('nicknames') != None and len(request.data.get('nicknames')) > 0:
		for nickname in request.data.get('nicknames'):
			nick = IngredientNickname(ingredient=ingredient,
				nickname=nickname)
			nick.save()
	
	return Response(status=200)

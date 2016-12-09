from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from .models import Ingredient, IngredientNickname, Recipe, RecipeImage, RecipeStep, RecipeIngredient
from .api import IngredientApi, RecipeApi
from django.contrib.auth.models import User
from django.db import connection

import json

@api_view(['GET','POST'])
def list_recipe(request):
    recipes = Recipe.objects.all()
    if request.GET.get('q'):
        recipes = recipes.filter(description__icontains=request.GET.get('q'))
    if request.GET.get('id'):
        recipes = recipes.filter(id=request.GET.get('id'))
    if request.GET.get('title'):
        recipes = recipes.filter(title__icontains=request.GET.get('title'))
    if request.data.get('ingredients'):
        rows_returned = SelectRecipeIdFromIngredient(request.data.getlist('ingredients'), 0)
        append(rows_returned, SelectRecipeIdFromIngredient(request.data.getlist('ingredients'), 1))
        append(rows_returned, SelectRecipeIdFromIngredient(request.data.getlist('ingredients'), 2))
        recipes = recipes.filter(id__in=rows_returned)
    api_return = RecipeApi(recipes, many=True)

    if len(recipes) == 0:
        return Response([], status=404)
    else:
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
    except ObjectDoesNotExist:
        return Response({"error":"Creator not found or not exist!"}, status=404)
    except:
        return Response({"error":"Unexpected error!"}, status=500)

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
                return Response({"error":"Ingredient %s has no description in how to use!" % ingredient['ingredient_id']}, status=500)
        except:
            return Response({"error":"Ingredient %s miss the attribute description!" % ingredient['ingredient_id']}, status=500)
        
        try:
            model = Ingredient.objects.get(pk=ingredient['ingredient_id'])
        except:
            return Response({"error":"Ingredient %s not found or not exist!" % ingredient['ingredient_id']}, status=404)

        ing = RecipeIngredient(description=ingredient["description"],
            ingredient=model,
            recipe=recipe)
        ing.save()

    return Response(status=200)

@api_view(['PUT',])
def update_recipe(request):
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
    if not request.data.get('id'):
        data.append({"error" : "you must inform the id of the reipce."})
    
    if len(data) > 0:
        return Response(data, status=400)

    try:
        creator = User.objects.get(pk=request.data.get('creator_id'))
    except ObjectDoesNotExist:
        return Response({"error":"Creator not found or not exist!"}, status=404)
    except:
        return Response({"error":"Unexpected error!"}, status=500)


    try:
        recipe = Recipe.objects.get(id=request.data.get('id'))
    except ObjectDoesNotExist:
        return Response({"error":"Recipe not found or not exist!"}, status=404)
    except:
        return Response({"error":"Unexpected error!"}, status=500)

    if recipe == None:
        data.append({'error':'Recipe was not found for edit!'})
        return Response(data, status=404)

    recipe = Recipe(id=request.data.get('id'),
        title=request.data.get('title'),
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
    old_steps = RecipeStep.objects.filter(recipe__id=request.data.get('id'))
    for old_step in old_steps:
        old_step.delete()
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
                return Response({"error":"Ingredient %s has no description in how to use!" % ingredient['ingredient_id']}, status=500)
        except:
            return Response({"error":"Ingredient %s miss the attribute description!" % ingredient['ingredient_id']}, status=500)
        
        try:
            model = Ingredient.objects.get(pk=ingredient['ingredient_id'])
        except:
            return Response({"error":"Ingredient %s not found or not exist!" % ingredient['ingredient_id']}, status=404)

        ing = RecipeIngredient(description=ingredient["description"],
            ingredient=model,
            recipe=recipe)
        ing.save()

    return Response(status=200)


def SelectRecipeIdFromIngredient(list_ingredient, quantity_missing):
    with connection.cursor() as cursor:
        where_ingredients = 'WHERE TAB_F.COUNT = {0}'
        if quantity_missing == 0:
            where_ingredients = where_ingredients.format(len(list_ingredient))
        elif quantity_missing == 1:
            where_ingredients = where_ingredients.format(len(list_ingredient) - 1)
        elif quantity_missing == 2:
            where_ingredients = where_ingredients.format(len(list_ingredient) - 2)
        cursor.execute('''
        SELECT TAB_F.ID
        FROM (SELECT COUNT(1) AS COUNT, TAB.RECIPE_ID AS ID
              FROM (SELECT DISTINCT RECIPE_ID, ingredient_id
                      FROM objetos_recipeingredient
                     WHERE INGREDIENT_ID IN ({0})
                     GROUP BY RECIPE_ID, INGREDIENT_ID) TAB
             GROUP BY RECIPE_ID) TAB_F
        {1}'''.format(str(list_ingredient).replace('[','').replace(']',''), where_ingredients)
        )
        row = cursor.fetchone()
    return row

def append(item, new_itens):
    if new_itens != None:
        if item != None:
            item += new_itens
        else:
            item = new_itens
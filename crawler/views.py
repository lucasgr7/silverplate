from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseServerError
from django.views.generic import ListView
from django.shortcuts import render

import urllib.request

from .models import IngredientSpec, IgnoredWords, DataWayCooking
from objetos.models import Ingredient, IngredientNickname, Recipe, RecipeStep, RecipeIngredient
from django.contrib.auth.models import User
from crawler.engine import LinkFinder
from crawler.engine import IngredientFinder
from crawler.engine import DataMining
from crawler.models import DataIngredient



# Create your views here.
class IngredientSpecList(ListView):
    context_object_name = 'ingredients'
    ordering = '-count'
    model = IngredientSpec
    paginate_by = 10

def home(request):
    return render(request, 'crawler/home.html')


def salvar_palavra_ignorar(request):
    if request.method == 'POST':
        word = request.POST.get('word')
        word = word.strip()
        if not ignore_word_exists(word):
            update_spec(word)
            Ignorar = IgnoredWords(word=word)
            Ignorar.save()

            Ingredients = Ingredient.objects.all()
            for ing in Ingredients:
                clear_specs(ing.description)

    return HttpResponseRedirect('/crawl/list')


def delete_spec(request):
    if request.method == 'POST':
        spec_id = request.POST.get('id')
        word = request.POST.get('word')
        spec = IngredientSpec(id=spec_id, word=word)
        spec.delete()

    return HttpResponseRedirect('/crawl/list')


def salvar_Ingrediente(request):
    if request.method == 'POST':
        new_ingredient = request.POST.get('word')
        ing = Ingredient(description=new_ingredient.title())
        ing.save()

        clear_specs(new_ingredient)
    return HttpResponseRedirect('/crawl/list')


def update_spec(pal_ignorar):
    list_ingredients = IngredientSpec.objects.order_by('-count')
    for Ingredient in list_ingredients:
        Ingredient.word = Ingredient.word.replace(pal_ignorar, '').strip()
        Ingredient.save()


def ignore_word_exists(word):
    return IgnoredWords.objects.filter(word=word).exists()


def clear_specs(new_ingredient):
    try:
        delete_list = IngredientSpec.objects.filter(word=new_ingredient.lower())
        for spec in delete_list:
            spec.delete()
    except IngredientSpec.DoesNotExist:
        print('sem chance')

def run_crawler(request):
    message = 'Finished the proccess'
    if request.method == 'POST':
        link = request.POST.get('url')
        number_access = request.POST.get('number_access')
        print('link : ' + link)
        if not number_access or number_access == None or number_access == '':
            message = 'You must inform number of access'
        if not link or number_access == None:
            message = 'You must inform the link to start crawling'
        if len(link) > 0:    
            try:
                #process to gather data from website
                number_access = int(number_access)
                response = urllib.request.urlopen(link)
                html = response.read().decode('utf-8')
                parser = LinkFinder()
                parser.feed(html)
                i = 0
                while number_access > 0:
                    link = parser.links[i]
                    print(link)
                    print('number_access ' + str(number_access))
                    response = urllib.request.urlopen(link)
                    html = response.read().decode('utf-8')
                    parser.feed(html)
                    i += 1
                    number_access -= 1

                print('links encontrados : ' + str(len(parser.links)))
                print('Will start recovering data from the site')

                DataParser = IngredientFinder()
                size = len(parser.links)
                for link in parser.links:
                    size -= 1
                    response = urllib.request.urlopen(link)
                    html = response.read().decode('utf-8')
                    DataParser.feed(html)

                print('Found %s ingredients' % DataParser.ingredientes)
                print('Found %s Steps Cooking' % DataParser.passos)
                #Mining the data
                mining = DataMining()
                ingredients = DataIngredient.objects.all()
                count = 0
                for ingredient in ingredients:
                    mining.analysis(ingredient.ingredient)
                    count += 1

                mining.save_to_db()
            except Exception as e:
                message = str(e)            

    return render(request, 'crawler/home.html', {'message':message})

def vinculate(request):
    try:
        ing_origin = request.POST.get('ingredient_origin').strip()
        nickname = request.POST.get('nickname').strip()
        if ing_origin == None or ing_origin == 0:
            return HttpResponseServerError("Invalid Ingredient id, it can't be null or invalid")
        if nickname == None or nickname == '':
            return HttpResponseServerError("Invalid Nickname, it can't be empty")

        ingredient_origin = Ingredient.objects.get(pk=ing_origin)
        if ingredient_origin == None:
            return HttpResponseServerError("Ingredient id doest not exist")
        ingredientNickname = IngredientNickname(ingredient=ingredient_origin,nickname=nickname)
        ingredientNickname.save()
        clear_specs(nickname)

        return HttpResponseRedirect('/crawl/list')
    except:
        return HttpResponseServerError("Error during process")

def save_recipe(request):
    user = User.objects.get(pk=1)
    recipes_raw = DataWayCooking.objects.values('recipe').distinct()
    for object_recipe in recipes_raw:
        recipe = str(object_recipe['recipe'])
        modelRecipe = Recipe(
            language='PT',
            title=recipe,
            description=recipe,
            creator = user
            )
        steps = ''
        modelRecipe.save()

        steps = DataWayCooking.objects.filter(recipe__contains=recipe).values('description')
        for step in steps:
            if step != None:
                ModelStep = RecipeStep(recipe=modelRecipe, step=step['description'].encode('UTF-8'))
                ModelStep.save()
        
        ingredients = Ingredient.objects.all()
        ingredientsData = DataIngredient.objects.filter(recipe__contains=recipe).values('ingredient')
        for dataIngredient in ingredientsData:
            if dataIngredient != None:
                for ingredientModel in ingredients:
                    found = False
                    if ingredientModel.description.upper() in dataIngredient['ingredient'].upper():
                        recipe_ingredient = RecipeIngredient(ingredient=ingredientModel,
                            recipe=modelRecipe,
                            description=dataIngredient['ingredient'].encode('UTF-8'))
                        recipe_ingredient.save()
                        found = True
                    if not found:
                        nicknames = IngredientNickname.objects.filter(ingredient_id=ingredientModel.id)
                        for nick in nicknames:
                            if nick.nickname.upper() in dataIngredient['ingredient'].upper():
                                recipe_ingredient = RecipeIngredient(ingredient=ingredientModel,
                                    recipe=modelRecipe,
                                    description=dataIngredient['ingredient'].encode('UTF-8'))
                                recipe_ingredient.save()
                                found = True
                    if found:
                        break



    
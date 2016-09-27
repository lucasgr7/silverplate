from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.shortcuts import render

import urllib.request

from .models import IngredientSpec, IgnoredWords
from objetos.models import Ingredient
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

    return HttpResponseRedirect('/crawl')


def salvar_Ingrediente(request):
    if request.method == 'POST':
        new_ingredient = request.POST.get('word')
        ing = Ingredient(description=new_ingredient.title())
        ing.save()

        clear_specs(new_ingredient)
    return HttpResponseRedirect('/crawl')


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
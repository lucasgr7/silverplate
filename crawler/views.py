from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.shortcuts import render

from .models import IngredientSpec, IgnoredWords
from objetos.models import Ingredient


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

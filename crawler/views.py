from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Ingredient_Spec, Ignore_Words
from objetos.models import Ingredient


# Create your views here.
def index(request):
    lista = Ingredient_Spec.objects.order_by('-Count')[:20]
    return render(request, 'index.html', {'lista': lista})


def salvar_palavra_ignorar(request):
    if request.method == 'POST':
        word = request.POST.get('word')
        word = word.strip()
        if not exists_palavra_ignorar(word):
            update_spec(word)
            Ignorar = Ignore_Words(Word=word)
            Ignorar.save()

            Ingredients = Ingredient.objects.all()
            for ing in Ingredients:
                clear_specs(ing.description)

    return HttpResponseRedirect('/crawl')


def delete_spec(request):
    if request.method == 'POST':
        spec_id = request.POST.get('id')
        word = request.POST.get('word')
        spec = Ingredient_Spec(id=spec_id, Word=word)
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
    list_ingredients = Ingredient_Spec.objects.order_by('-Count')
    for Ingredient in list_ingredients:
        Ingredient.Word = Ingredient.Word.replace(pal_ignorar, '').strip()
        print(Ingredient)
        Ingredient.save()


def exists_palavra_ignorar(word):
    try:
        existe_palavra = Ignore_Words.objects.get(Word=word)
        return 1
    except Ignore_Words.DoesNotExist:
        return 0


def clear_specs(new_ingredient):
    try:
        print(new_ingredient.title())
        delete_list = Ingredient_Spec.objects.filter(Word=new_ingredient.lower())
        for spec in delete_list:
            spec.delete()
    except Ingredient_Spec.DoesNotExist:
        print('sem chance')

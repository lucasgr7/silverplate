from django.test import TestCase
from django.test import Client
from django.db import transaction
from django.contrib.auth.models import User

from objetos.models import Ingredient, Recipe, RecipeImage,RecipeIngredient, RecipeStep
from .base_test import BaseTest
import json


class RecipeApiPutTest(BaseTest):
    c = Client(enforce_csrf_checks=False)

    @classmethod
    def setUpClass(cls):
        #mock
        u = User(username='username 01',password='123')
        u.save()
        i = Ingredient(description="Ingredient 1", image="1")
        i.save()

        r = Recipe(title='recipe 1',creator=u,description='recipe 1 description',language='pt')
        r.save()

        rIng = RecipeIngredient(ingredient=i,
        recipe=r,
        description='use this ingredient')
        rIng.save()

        s = RecipeStep(order=1,
        step='do this to work the recipe',recipe=r)
        s.save()

       

    @classmethod
    def tearDownClass(cls):        
        cls.clear_test(cls)
        print("ending")

    def test_recipe_put(self):
        recipe = Recipe.objects.get(title='recipe 1')
        creator = User.objects.get(username='username 01')
        response = self.c.put('/api/recipe/update',json.dumps({'title':'recipe changed',
            'creator_id' : creator.id,
            'description' : recipe.description,
            'language' : recipe.language
            }),content_type='application/json',
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        print(response.data)

        self.assertEqual(response.status_code, 200)

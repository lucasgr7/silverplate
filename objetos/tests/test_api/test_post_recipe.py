from django.test import TestCase
from django.test import Client
from django.db import transaction
from django.contrib.auth.models import User

from objetos.models import Ingredient, Recipe, RecipeImage,RecipeIngredient, RecipeStep
from .base_test import BaseTest
import json



class IngredientApiTestGet(BaseTest):
    c = Client(enforce_csrf_checks=False)
    @classmethod
    def setUpClass(cls):
        #mock
        u = User(username='username 01',password='123')
        u.save()
        i = Ingredient(description="Ingredient 1", image="1")
        i.save()

    @classmethod
    def tearDownClass(cls):
        cls.clear_test(cls)
        print('end of tests')

    def test_save_success(self):
        creator = User.objects.get(username='username 01')
        ingredients = Ingredient.objects.all()
        recipes = Recipe.objects.all()

        self.assertEqual(len(recipes), 0)
        response = self.c.post('/api/recipe/save',json.dumps({
            'title':'recipe new',
            'creator_id' : creator.id,
            'description' : 'new recipe',
            'language' : 'PT-br',
            'steps' : [{'order': 1, 'step' : 'new step'},{'order': 2, 'step' : 'new step 2'}],
            'ingredients' : list(
                    map(lambda x : {'ingredient_id' : x.id, 'description' : x.description}, ingredients)
                )
            }),content_type='application/json')
        
        self.assertEqual(response.status_code, 200)

        recipes = Recipe.objects.all()
        self.assertEqual(len(recipes), 1)

    def test_save_no_title(self):
        print('123')

    def test_save_no_ingredient(self):
        print('123')

    def test_save_no_step(self):
        print('123')
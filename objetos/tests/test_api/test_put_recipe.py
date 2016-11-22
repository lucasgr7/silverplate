from django.test import TestCase
from django.test import Client
from django.db import transaction
from django.contrib.auth.models import User

from objetos.models import Ingredient, Recipe, RecipeImage,RecipeIngredient, RecipeStep
import json


class RecipeApiPutTest(TestCase):
    c = Client(enforce_csrf_checks=False)
    rIng2 = {}
    @classmethod
    def setUpClass(cls):
    #mock
    print('starting')
       

    @classmethod
    def tearDownClass(cls):
        print('end of tests')

    def test_recipe_put(self):
        self.assertEqual(1==1)

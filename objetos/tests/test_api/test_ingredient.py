from django.test import TestCase
from django.test import Client
from django.db import transaction

from objetos.models import Ingredient
from .base_test import BaseTest
import json


class IngredientApiTestGet(BaseTest):
    c = Client(enforce_csrf_checks=False)
    @classmethod
    def setUpClass(cls):
        #mock
        i = Ingredient(description="Ingredient 1", image="1")
        i.save()
        i = Ingredient(description="Ingredient 2", image="2")
        i.save()
        i = Ingredient(description="Ingredient 3", image="3")
        i.save()

    @classmethod
    def tearDownClass(cls):
        cls.clear_test(cls)
        print('end of tests')

    def test_ingredient_Get(self):
        response = self.c.get('/api/ingredient', {})
        self.assertEqual(len(Ingredient.objects.all()), 3)
        self.assertEqual(response.status_code, 200)


    def test_ingredient_Post(self):
        response = self.c.post('/api/ingredient/save', {'description':'new ingredient','image':'image.com/123'})
        self.assertEqual(len(Ingredient.objects.all()), 4)
        self.assertEqual(response.status_code, 200)

    def test_ingredient_Put(self):
        ingredient = Ingredient.objects.get(description='Ingredient 1')
        response = self.c.put('/api/ingredient/update', 
            json.dumps({"id":ingredient.id,"description":"changed","image":"changed_image"}),
            content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(len(Ingredient.objects.all()), 3)
        self.assertEqual(response.status_code, 200)
        ingredient_changed = Ingredient.objects.get(pk=ingredient.id)
        self.assertEqual(ingredient_changed.description, 'changed')
        self.assertEqual(ingredient_changed.image, 'changed_image')

    def test_ingredient_Delete(self):
        ingredient = Ingredient.objects.get(description='Ingredient 2')
        response = self.c.delete('/api/ingredient/delete?id=%s' % ingredient.id)
        self.assertEqual(len(Ingredient.objects.all()), 2)
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Exception) as context:
            ingredient_deleted = Ingredient.objects.get(pk=2) 

            self.assertTrue('matching query does not exists' in context.exception)

    def test_ingredient_Post_no_image(self):
        response = self.c.post('/api/ingredient/save', {'description':'new ingredient'})
        self.assertEqual(len(Ingredient.objects.all()), 3)
        self.assertEqual(response.status_code, 400)

    def test_ingredient_Delete_non_Existent(self):
        response = self.c.delete('/api/ingredient/delete?id=9999')
        self.assertEqual(len(Ingredient.objects.all()), 3)
        self.assertEqual(response.status_code, 404)

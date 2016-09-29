from django.test import TestCase
from django.test import Client
from django.db import transaction

from ...views import IngredientSpecList
from objetos.models import IngredientNickname, Ingredient


class VinculateIngredientTests(TestCase):

    def test_send_id_null(self):
        c = Client(enforce_csrf_checks=False)
        response = c.post('/crawl/vinculate', {'ingredient_origin':None, 'nickname':'eggs'})
        self.assertEqual(len(IngredientNickname.objects.all()), 0)
        self.assertEqual(response.status_code, 500)


    def test_send_nickname_null(self):
        obj_ing = Ingredient(description='Egg',image='http://image.jpeg')
        obj_ing.save()
        ingredient_pk = Ingredient.objects.get(description=obj_ing.description).id

        c = Client(enforce_csrf_checks=False)
        response = c.post('/crawl/vinculate', {'ingredient_origin':1, 'nickname':None})
        self.assertEqual(len(IngredientNickname.objects.all()), 0)
        self.assertEqual(response.status_code, 500)

    def test_send_nickname_empty(self):
        obj_ing = Ingredient(description='Egg',image='http://image.jpeg')
        obj_ing.save()
        ingredient_pk = Ingredient.objects.get(description=obj_ing.description).id

        c = Client(enforce_csrf_checks=False)
        response =  c.post('/crawl/vinculate', {'ingredient_origin':1, 'nickname':' '})
        self.assertEqual(len(IngredientNickname.objects.all()), 0)
        self.assertEqual(response.status_code, 500)

    def test_vinculate_success(self):
        obj_ing = Ingredient(description='Egg',image='http://image.jpeg')
        obj_ing.save()
        ingredient_pk = Ingredient.objects.get(description=obj_ing.description).id

        c = Client(enforce_csrf_checks=False)
        response = c.post('/crawl/vinculate', {'ingredient_origin':ingredient_pk, 'nickname':'eggs'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(IngredientNickname.objects.all()), 1)

    def test_vinculate_avoid_duplication(self):
        obj_ing = Ingredient(description='Egg',image='http://image.jpeg')
        obj_ing.save()
        ingredient_pk = Ingredient.objects.get(description=obj_ing.description).id

        c = Client(enforce_csrf_checks=False)
        response = c.post('/crawl/vinculate', {'ingredient_origin':ingredient_pk, 'nickname':'eggs'})
        dir(response)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(IngredientNickname.objects.all()), 1)

        with transaction.atomic():
            response = c.post('/crawl/vinculate', {'ingredient_origin':1, 'nickname':'eggs'})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(len(IngredientNickname.objects.all()), 1)


    def test_not_exists_ingredient_id(self):
        obj_ing = Ingredient(description='Egg',image='http://image.jpeg')
        obj_ing.save()
        ingredient_pk = Ingredient.objects.get(description=obj_ing.description).id

        c = Client(enforce_csrf_checks=False)
        response =  c.post('/crawl/vinculate', {'ingredient_origin':9999, 'nickname':' '})
        self.assertEqual(len(IngredientNickname.objects.all()), 0)
        self.assertEqual(response.status_code, 500)
from django.test import TestCase
from django.test import Client
from django.db import transaction
from django.contrib.auth.models import User

from objetos.models import Ingredient, Recipe, RecipeImage,RecipeIngredient, RecipeStep
import json


class RecipeApiTest(TestCase):
    c = Client(enforce_csrf_checks=False)
    rIng2 = {}
    @classmethod
    def setUpClass(cls):
        #mock
        u = User(username='username 01',password='123')
        u.save()
        u = User(username='username 02',password='123')
        u.save()

        i = Ingredient(description="Ingredient 1", image="1")
        i.save()
        i2 = Ingredient(description="Ingredient 2", image="2")
        i2.save()
        i3 = Ingredient(description="Ingredient 3", image="3")
        i3.save()
        i4 = Ingredient(description="Ingredient 4", image="4")
        i4.save()

        r = Recipe(title='recipe 1',
            creator=u,
            description='recipe 1 description',
            language='pt')
        r.save()
        r2 = Recipe(title='recipe 2',
            creator=u,
            description='recipe 2 description',
            language='pt')
        r2.save()
        r3 = Recipe(title='recipe 3',
            creator=u,
            description='recipe 3 description',
            language='pt')
        r3.save()
        r4 = Recipe(title='recipe 4',
            creator=u,
            description='recipe 4 description',
            language='pt')
        r4.save()
        r5 = Recipe(title='recipe 5',
            creator=u,
            description='recipe 5 description',
            language='pt')
        r5.save()

        ri = RecipeImage(description='image for recipe 01',
            url='http://site.com/image.jpeg',
            recipe=r)
        ri.save()
        ri = RecipeImage(description='image for recipe 02',
            url='http://site.com/image.jpeg',
            recipe=r2)
        ri.save()


        #recipe 1
        rIng = RecipeIngredient(ingredient=i,
            recipe=r,
            description='use this ingredient')
        rIng.save()
        #recipe 2
        rIng2 = RecipeIngredient(ingredient=i2,
            recipe=r2,
            description='use this ingredient 2')
        rIng2.save()
        #recipe 3
        rIng3 = RecipeIngredient(ingredient=i,
            recipe=r3,
            description='use this ingredient 1 for recipe 3')
        rIng3.save()
        rIng4 = RecipeIngredient(ingredient=i2,
            recipe=r3,
            description='use this ingredient 2 for recipe 3')
        rIng4.save()
        #recipe 4
        rIng5 = RecipeIngredient(ingredient=i2,
            recipe=r4,
            description='use this ingredient 2 for recipe 4')
        rIng5.save()
        rIng6 = RecipeIngredient(ingredient=i3,
            recipe=r4,
            description='use this ingredient 3 for recipe 4')
        rIng6.save()
        rIng7 = RecipeIngredient(ingredient=i,
            recipe=r4,
            description='use this ingredient 1 for recipe 4')
        rIng7.save()
        #recipe 5
        rIng8 = RecipeIngredient(ingredient=i,
            recipe=r5,
            description='use this ingredient 1 for recipe 5')
        rIng8.save()
        rIng9 = RecipeIngredient(ingredient=i2,
            recipe=r5,
            description='use this ingredient 2 for recipe 5')
        rIng9.save()
        rIng10 = RecipeIngredient(ingredient=i3,
            recipe=r5,
            description='use this ingredient 3 for recipe 5')
        rIng10.save()
        rIng11 = RecipeIngredient(ingredient=i4,
            recipe=r5,
            description='use this ingredient 4 for recipe 5')
        rIng11.save()

        s = RecipeStep(order=1,
            step='do this to work the recipe',
            recipe=r)
        s.save()
        s = RecipeStep(order=1,
            step='do this to work the recipe 2',
            recipe=r2)
        s.save()

        s = RecipeStep(order=1,
            step='do this to work the recipe 3',
            recipe=r3)
        s.save()
        s = RecipeStep(order=1,
            step='do this to work the recipe 4',
            recipe=r4)
        s.save()

    @classmethod
    def tearDownClass(cls):
        print('end of tests')

    def test_recipe_Get(self):
        response = self.c.get('/api/recipe', {})
        self.assertEqual(len(Recipe.objects.all()), len(response.data))
        self.assertEqual(response.status_code, 200)

    def test_recipe_Get_dont_exist(self):
        response = self.c.get('/api/recipe?id=9999' )
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, 404)

    def test_recipe_Get_Id(self):
        response = self.c.get('/api/recipe?id=1&title=recipe 1' )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_recipe_Get_title(self):
        response = self.c.get('/api/recipe?title=recipe 1' )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_recipe_Get_filter_dont_match(self):
        response = self.c.get('/api/recipe?id=2&title=recipe 1' )
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, 404)

    def test_recipe_Get_filter_1_ingredient(self):
        RecipeIngredient2 = RecipeIngredient.objects.get(description='use this ingredient 2')
        response = self.c.post('/api/recipe', {'ingredients' : [RecipeIngredient2.ingredient.id]} )
        

        assert_recipe_2 = Recipe.objects.get(title='recipe 2')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], assert_recipe_2.id)
        self.assertEqual(response.status_code, 200)

    def test_recipe_Get_filter_2_ingredient(self):
        rIng1 = RecipeIngredient.objects.get(description='use this ingredient 1 for recipe 3')
        rIng2 = RecipeIngredient.objects.get(description='use this ingredient 2 for recipe 3')
        recipe = Recipe.objects.get(title='recipe 3')
        response = self.c.post('/api/recipe', {'ingredients' : [rIng2.ingredient.id, rIng1.ingredient.id]}) 
        #print(response.data)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], recipe.id)
        
        self.assertEqual(response.status_code, 200)

    def test_recipe_get_filter_2_ingredients_miss_1(self):
        rIng5 = RecipeIngredient.objects.get(description='use this ingredient 2 for recipe 4')
        rIng6 = RecipeIngredient.objects.get(description='use this ingredient 3 for recipe 4')
        recipe = Recipe.objects.get(title='recipe 4')

        response = self.c.post('/api/recipe', {'ingredients' : [rIng5.ingredient.id, rIng6.ingredient.id]}) 

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], recipe.id)
        
        self.assertEqual(response.status_code, 200)

    def test_recipe_get_filter_2_ingredients_miss_2(self):
        rIng5 = RecipeIngredient.objects.get(description='use this ingredient 3 for recipe 5')
        rIng6 = RecipeIngredient.objects.get(description='use this ingredient 4 for recipe 5')
        recipe = Recipe.objects.get(title='recipe 5')

        response = self.c.post('/api/recipe', {'ingredients' : [rIng5.ingredient.id, rIng6.ingredient.id]}) 

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], recipe.id)
        
        self.assertEqual(response.status_code, 200)
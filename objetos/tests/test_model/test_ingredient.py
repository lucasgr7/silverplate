from django.test import TestCase

from objetos.models import Ingredient


class IngredientTestCase(TestCase):
    def test_str(self):
        ingredient = Ingredient.objects.create(description='Some description')

        self.assertIsInstance(ingredient, Ingredient)
        self.assertEqual(ingredient.description, str(ingredient))

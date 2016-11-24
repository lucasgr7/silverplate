from django.test import TestCase
from django.contrib.auth.models import User

from objetos.models import Ingredient, Recipe, RecipeImage,RecipeIngredient, RecipeStep
import json


class BaseTest(TestCase):
	def clear_test(self):
		for u in User.objects.all():
			u.delete()

		for i in Ingredient.objects.all():
			i.delete()

		for r in Recipe.objects.all():
			r.delete()

		for ri in RecipeIngredient.objects.all():
			ri.delete()

		for s in RecipeStep.objects.all():
			s.delete()

		for rim in RecipeImage.objects.all():
			rim.delete()




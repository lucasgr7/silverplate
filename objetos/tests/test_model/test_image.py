from django.test import TestCase

from objetos.models import Image


class IngredientTestCase(TestCase):
    def test_str(self):
        image = Image.objects.create(description='Some description')

        self.assertIsInstance(image, Image)
        self.assertEqual(image.description, str(image))

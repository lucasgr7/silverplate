from django.test import TestCase
from django.contrib.auth.models import User

from objetos.models import Comment


class IngredientTestCase(TestCase):
    def test_str(self):
        user = User.objects.create()
        comment = Comment.objects.create(message='Some description', creator=user)

        self.assertIsInstance(comment, Comment)
        self.assertEqual(comment.message, str(comment))

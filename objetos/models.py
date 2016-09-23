from django.db import models
from django.contrib.auth.models import User



class Ingredient(models.Model):
    description = models.TextField()
    image = models.CharField(max_length=500)

    def __str__(self):
        return self.description

class IngredientNickname(models.Model):
    ingredient = models.ForeignKey(Ingredient)
    nickname = models.CharField(max_length=128, db_index=True)

class Image(models.Model):
    description = models.CharField(max_length=150)
    url = models.URLField()

    def __str__(self):
        return self.description


class Recipe(models.Model):
    LANG = (('EN', "English"), ('PT', "Portuguese"))

    title = models.CharField(max_length=128, db_index=True)
    step = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ManyToManyField(Image)
    description = models.TextField()
    language = models.CharField(max_length=10, choices=LANG)

    def __str__(self):
        return self.description


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient)
    recipe = models.ForeignKey(Recipe)
    description = models.TextField()


class RecipeStep(models.Model):
    '''Class with instructions step by step how to cook'''
    step = models.CharField(max_length=500)
    recipe = models.OneToOneField(Recipe)


class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return self.message

    def short_message(self):
        if not self.message or len(self.message) < 15:
            return self.message
        return self.message[:15] + '...'

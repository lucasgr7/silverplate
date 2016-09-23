from django.db import models


class DataIngredient(models.Model):
    """"Class used to Store Ingredients of the recipes found in the crawling process"""

    ingredient = models.CharField(max_length=1000)
    recipe = models.CharField(max_length=500)
    group = models.CharField(max_length=500, default='Ingredientes')

    def __str__(self):
        return self.ingredient


class DataWayCooking(models.Model):
    """Class used to Store steps of the recipes found in the crawling process"""
    description = models.CharField(max_length=500)
    recipe = models.CharField(max_length=500)
    group = models.CharField(max_length=500, default='Modo de Fazer')

    def __str__(self):
        return self.description


class IngredientSpec(models.Model):
    """Class used to manipulate Ingredients found and change data to data mining and found patterns of ingredients"""
    word = models.CharField(max_length=500, db_index=True)
    count = models.IntegerField(default=0)
    type = models.CharField(max_length=1)


class IngredientNickname(models.Model):
    ingredient = models.ForeignKey(IngredientSpec)
    nickname = models.CharField(max_length=128, db_index=True)


class IgnoredWords(models.Model):
    """Model to store words to ignore from Ingredient Spec"""
    word = models.CharField(max_length=500, db_index=True)

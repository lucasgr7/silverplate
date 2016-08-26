from django.contrib import admin
from .models import Ingredient, Image, Recipe, Comment

admin.site.register(Ingredient)

admin.site.register(Image)

admin.site.register(Recipe)

admin.site.register(Comment)

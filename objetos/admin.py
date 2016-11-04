from django.contrib import admin
from .models import Ingredient, RecipeImage, Recipe, Comment


admin.site.register(Ingredient)

admin.site.register(RecipeImage)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'language']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['short_message', 'creator', 'created_at', 'modified_at']

from django.conf.urls  import include, url, patterns
from . import views_ingredient, views_recipe

urlpatterns = [
    url(r'^ingredient$', views_ingredient.list_ingredient, name='listar_ingredient'),
    url(r'^ingredient/save$', views_ingredient.save_ingredient, name='save_ingredient'),
    url(r'^ingredient/delete$', views_ingredient.delete_ingredient, name='delete_ingredient'),
    url(r'^ingredient/update$', views_ingredient.update_ingredient, name='update_ingredient'),
    url(r'^recipe$', views_recipe.list_recipe, name='listar_recipe'),
]

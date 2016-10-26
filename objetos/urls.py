from django.conf.urls  import include, url, patterns
from . import views

urlpatterns = [
    url(r'^ingredient$', views.list_ingredient, name='listar_ingredient'),
    url(r'^ingredient/save$', views.save_ingredient, name='save_ingredient'),
    url(r'^recipe$', views.list_recipe, name='listar_recipe'),
]

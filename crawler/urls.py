from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^list$', views.IngredientSpecList.as_view(), name='ingredient_list'),
    url(r'^salvar_palavra_ignorar$', views.salvar_palavra_ignorar, name='salvar_palavra_ignorar'),
    url(r'^salvar_ingrediente$', views.salvar_Ingrediente, name='salvar_ingrediente'),
    url(r'^delete_spec$', views.delete_spec, name='salvar_ingrediente'),
    url(r'^run_crawler$', views.run_crawler, name='run_crawler'),
]

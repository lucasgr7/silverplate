from django.conf.urls  import include, url, patterns
from . import views

urlpatterns = [
    url(r'^ingredient$', views.list_ingredient, name='listar_ingredient'),
]

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^crawl/', include('crawler.urls', namespace='crawl')),
    url(r'^api/', include('objetos.urls', namespace='objetos')),

    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^contact$', TemplateView.as_view(template_name='contact.html'), name='contact'),
    url(r'^about', TemplateView.as_view(template_name='about.html'), name='about')
]

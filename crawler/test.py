from django.test import TestCase
from django.test import TestCase
from crawler.LinkFinder import LinkFinder
from crawler.DataFinder import IngredienteFinder
from crawler.models import Dados_Ingrediente
from crawler.DataMining import Data_Mining
import urllib.request


# Create your tests here.
class CrawlerTestCase(TestCase):
    def test_links_finder_count(self):
        """Test the count of links in link finder is equal to the expected amount"""
        finder = LinkFinder()
        html = '<html><a href="http://comidaereceitas.com/teste">Link 01</a><span>Span no meio</span><a href="' \
               'http://comidaereceitas.com/teste2">Link 02</a></html>'
        finder.feed(html)
        self.assertEqual(2, len(finder.links))

    def test_push_sem_duplicado(self):
        """Test if the method in link finder (push) do not let have duplicate values for the links finded"""
        finder = LinkFinder()
        finder.push('goku')
        finder.push('vegeta')
        finder.push('goku')
        self.assertEqual(2, len(finder.links))

    def test_ingredients_found(self):
        """Evaluate if the quantity of ingredients found on in a page is equal to the real amount expected"""
        finder = IngredienteFinder()
        link = 'https://www.comidaereceitas.com.br/bolos/bolo-felpudo-de-coco.html'
        response = urllib.request.urlopen(link)
        html = response.read().decode('utf-8')
        finder.feed(html)
        self.assertEqual(12, finder.ingredientes)

    def test_way_cooking_found(self):
        """Evaluate if the quantity of way of cooking found on in a page is equal to the real amount expected"""
        finder = IngredienteFinder()
        link = 'https://www.comidaereceitas.com.br/bolos/bolo-felpudo-de-coco.html'
        response = urllib.request.urlopen(link)
        html = response.read().decode('utf-8')
        finder.feed(html)
        self.assertEqual(8, finder.passos)

    def test_filter_only_recipe(self):
        """Evaluate if the Data Finder only download data from pages evaulated as real recipes and not info pages"""
        finder = IngredienteFinder()
        link = 'https://www.comidaereceitas.com.br/informacoes/politica-de-privacidade.html'
        response = urllib.request.urlopen(link)
        html = response.read().decode('utf-8')
        finder.feed(html)
        self.assertEqual(0, finder.ingredientes)

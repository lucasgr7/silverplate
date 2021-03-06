from django.test import TestCase
from crawler.engine import LinkFinder, IngredientFinder
import urllib.request

from ..models import DataIngredient


class CrawlerTestCase(TestCase):
    def test_links_finder_count(self):
        """Test the count of links in link finder is equal to the expected amount"""
        finder = LinkFinder()
        html = '<html><a href="http://comidaereceitas.com/teste">Link 01</a><span>Span no meio</span><a href="' \
               'http://comidaereceitas.com/teste2">Link 02</a></html>'
        finder.feed(html)
        self.assertEqual(2, len(finder.links))

    def test_push_sem_duplicates(self):
        """Test if the method in link finder (push) do not let have duplicate values for the links found"""
        finder = LinkFinder()
        finder.push('goku')
        finder.push('vegeta')
        finder.push('goku')
        self.assertEqual(2, len(finder.links))

    def test_ingredients_found(self):
        """Evaluate if the quantity of ingredients found on in a page is equal to the real amount expected"""
        finder = IngredientFinder()
        link = 'https://www.comidaereceitas.com.br/bolos/bolo-felpudo-de-coco.html'
        response = urllib.request.urlopen(link)
        html = response.read().decode('utf-8')
        finder.feed(html)
        self.assertEqual(12, finder.ingredientes, 'should be {}, is {}, stores in db {}'.format(
            12,
            finder.ingredientes,
            str(DataIngredient.objects.all())
        ))

    def test_way_cooking_found(self):
        """Evaluate if the quantity of way of cooking found on in a page is equal to the real amount expected"""
        finder = IngredientFinder()
        link = 'https://www.comidaereceitas.com.br/bolos/bolo-felpudo-de-coco.html'
        response = urllib.request.urlopen(link)
        html = response.read().decode('utf-8')
        finder.feed(html)
        self.assertEqual(8, finder.passos)

    def test_filter_only_recipe(self):
        """Evaluate if the Data Finder only download data from pages evaulated as real recipes and not info pages"""
        finder = IngredientFinder()
        link = 'https://www.comidaereceitas.com.br/informacoes/politica-de-privacidade.html'
        response = urllib.request.urlopen(link)
        html = response.read().decode('utf-8')
        finder.feed(html)
        self.assertEqual(0, finder.ingredientes)

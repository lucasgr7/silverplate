import os
import django
from collections import Counter
from html.parser import HTMLParser

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silverplate.settings")
django.setup()

from .models import DataIngredient, DataWayCooking, IngredientSpec


class LinkFinder(HTMLParser):
    """
    Class responsible for find new Links in HTML and store in a list 'self.links'
    Using the Python Standard Library HTML PARSER to read HTML data and identify patterns of regular data store on database
    https://docs.python.org/2/library/htmlparser.html
    """

    links = []

    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        if str(tag) == 'a':
            for attr in attrs:
                for inn in attr:
                    if inn != None and 'http' in inn and 'comidaereceitas.com' in inn and not 'whatsapp' in inn and not 'facebook' in inn and not 'twitter' in inn and not 'google' in inn and not 'pinterest' in inn:
                        self.push(inn)

    def push(self, link):
        if link not in self.links:
            self.links.append(link)


class IngredientFinder(HTMLParser):
    """
    Class responsible for find Data in the website that is being Crawled
    Using the Python Standard Library HTML PARSER to read HTML data and identify patterns of regular data store on database
    https://docs.python.org/2/library/htmlparser.html
    """
    recording = 0
    isMainText = 0
    isRecipeName = 0
    current_recipe = ""
    countDivs = 0
    countUl = 0
    ingredientes = 0
    passos = 0
    isGroup = 0
    isFoiModo_de_fazer = 0
    isCooking_Way = 0
    grupo = ''

    def __init__(self):
        HTMLParser.__init__(self)
        self.ingredientes = 0

    def handle_starttag(self, tag, attrs):
        if str(tag) == 'div':
            if self.search_class(attrs, 'maintext'):
                self.isMainText = 1
                self.countDivs = 2
        if str(tag) == 'strong' and self.isMainText:
            self.isGroup = 1

        elif str(tag) == 'td':
            if self.search_class(attrs, 'item contentheading'):
                self.isRecipeName = 1


        elif self.isMainText and str(tag) == 'ul':
            self.recording = 1
            self.countUl += 1

    def search_class(self, array, chave):
        for attr in array:
            for inn in attr:
                if str(inn) == chave:
                    return 1

    def handle_endtag(self, tag):
        if str(tag) == 'ul' and self.recording:
            self.recording = 0
        elif str(tag) == 'div' and self.isMainText:
            self.countDivs -= 1
            if self.countDivs == 0:
                self.isMainText = 0
                self.countUl = 0
        elif str(tag) == 'html':
            self.isCooking_Way = 0
        elif str(tag) == 'td' and self.isRecipeName:
            self.isRecipeName = 0
        elif str(tag) == 'strong' and self.isGroup:
            self.isGroup = 0

    def handle_data(self, data):
        if str(data).strip() != "":
            if self.recording == 1:
                # UL DOS INGREDIENTES
                if self.countUl >= 1 and not self.isCooking_Way:
                    if self.current_recipe != "" and "Receita" in self.current_recipe:
                        self.ingredientes += 1
                        DataIngredient.objects.create(ingredient=data, recipe=self.current_recipe, group=self.grupo)
                # F
                elif self.isCooking_Way:
                    if self.current_recipe != "":
                        self.passos += 1
                        DataWayCooking.objects.create(description=data, recipe=self.current_recipe, group=self.grupo)
            if self.isRecipeName:
                self.current_recipe = data
            if self.isGroup:
                self.grupo = data.strip()
                if self.grupo == 'Modo de preparo':
                    self.isCooking_Way = 1


class DataMining:
    """
    Class responsible for comparing replicated data and storing it in a special model IngredientSpec
    and a group counting repetitions
    """

    def __init__(self):
        self.words = Counter()

    def analysis(self, ingredient):
        self.save_words(ingredient.lower())

    def save_words(self, word):
        self.words[word] += 1

    def save_to_db(self):
        for word, count in self.words.items():
            try:
                ingredient = IngredientSpec.objects.get(word=word)
                ingredient.count += count
                ingredient.save()
            except IngredientSpec.DoesNotExist:
                IngredientSpec.objects.create(word=word, count=count, type='n')

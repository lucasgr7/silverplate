from html.parser import HTMLParser

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silverplate.settings")
import django

django.setup()

from crawler.models import Data_Ingredient, Data_Way_Cooking


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
                        data_save = Data_Ingredient(Ingredient=data, Recipe=self.current_recipe, Group=self.grupo)
                        data_save.save()
                # F
                elif self.isCooking_Way:
                    if self.current_recipe != "":
                        self.passos += 1
                        data_save = Data_Way_Cooking(Description=data, Recipe=self.current_recipe, Group=self.grupo)
                        data_save.save()
            if self.isRecipeName:
                self.current_recipe = data
            if self.isGroup:
                self.grupo = data.strip()
                if self.grupo == 'Modo de preparo':
                    self.isCooking_Way = 1

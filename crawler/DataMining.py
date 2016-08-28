class Word():
    value = ''
    count = 0

    def __init__(self, value):
        self.value = value
        self.count = 1


class Data_Mining():
    """
    Class responsible to compare replicated data and store in a special model Ingredient_Spec
    and agroup counting repetitions
    """
    list_words = set()

    def __init__(self):
        self.list_words = set()

    def Analysis(self, ingrediente):
        self.Save_word(ingrediente)

    def Save_word(self, word):
        encontrado = 0
        for p in self.list_words:
            if word == p.value:
                p.count += 1
                encontrado = 1

        if not encontrado:
            self.list_words.add(Word(value=word))

from html.parser import HTMLParser


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
                    if inn != None and 'http' in inn and 'comidaereceitas.com' in inn and not 'whatsapp' in inn and not 'facebook' in inn:
                        self.push(inn)

    def push(self, link):
        if link not in self.links:
            self.links.append(link)

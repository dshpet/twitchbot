from .BaseCommand import BaseCommand
from urllib import request
from bs4 import BeautifulSoup

class RandomPasta(BaseCommand):
    """Gets a random pasta text from selected web"""

    def perfrom(self, message, sender):
      raise RuntimeError("Not implemented")

    def respond(self, message, sender):
      url = "http://www.twitchquotes.com/random"
      pasta_site = request.urlopen(url)
      pasta_doc = pasta_site.read()
      soup = BeautifulSoup(pasta_doc, 'html.parser')
      real_pasta = soup.find(id="quote_content_1")
      pasta_text = str(real_pasta.contents[0]) # i don't like it but for simple purposes it works

      return pasta_text

    def __str__(self, **kwargs):
      return "Wanna see a good ol' random copypasta? Just do it"


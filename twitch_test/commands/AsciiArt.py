from .BaseCommand import BaseCommand
from urllib import request
from bs4 import BeautifulSoup
from random import choice

class AsciiArt(BaseCommand):
    """Gets a random donger face from selected web"""

    def perfrom(self, message, sender):
      raise RuntimeError("Not implemented")

    def respond(self, message, sender):
      url = "http://www.twitchquotes.com/copypastas/ascii-art"
      pasta_site = request.urlopen(url)
      pasta_doc = pasta_site.read()
      soup = BeautifulSoup(pasta_doc, 'html.parser')
      all_links = soup.find_all('a', {"class":"ascii_preview_link"})

      ascii_site = request.urlopen("http://www.twitchquotes.com/" + choice(all_links).attrs['href'])
      ascii_doc = ascii_site.read()
      ascii_soup = BeautifulSoup(ascii_doc, 'html.parser')
      art = ascii_soup.find(id = 'quote_content_0')
      
      return art.contents[0]

    def __str__(self, **kwargs):
      return "Wanna see a fancy donger? Type me"


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .BaseCommand import BaseCommand
from urllib import request
from bs4 import BeautifulSoup
from random import choice
from random import randint

class AsciiArt(BaseCommand):
    """Gets a random donger face from selected web"""

    def respond(self, message, sender):
      url = "http://www.twitchquotes.com/copypastas/ascii-art"
      page_specificator = "?page=" + str(randint(1, 6)) # well, life is not a rainbow field
      pasta_site = request.urlopen(url + page_specificator)
      pasta_doc = pasta_site.read()
      soup = BeautifulSoup(pasta_doc, 'html.parser')

      # button "copy to clipboard" is javascript-based and i cant parse it easily
      all_pasta_containers = soup.find_all('div', class_ = 'quote-content-parent')

      random_pasta_container = choice(all_pasta_containers)

      # fuck sites scraping 
      image = random_pasta_container.find('img')      
      text = ""
      if image != None:
        text = image['alt']
      else:
        text = random_pasta_container.text[19:-4] 
      
      text = text.replace("\r", "")
      text = text.replace("\n", "")

      return text

    def __str__(self, **kwargs):
      return "Wanna see a fancy donger? Type me"

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .BaseCommand import BaseCommand
from urllib import request
from bs4 import BeautifulSoup
from random import choice

class DongerFace(BaseCommand):
    """Gets a random donger face from selected web"""

    def respond(self, message, sender):
      url = "http://textfac.es"
      req = request.Request(url, headers={'User-Agent' : "Magic Browser"}) # blockers DansGame
      pasta_site = request.urlopen(req)
      pasta_doc = pasta_site.read()
      soup = BeautifulSoup(pasta_doc, 'html.parser')
      faces = soup.find_all('button', {"class":"facebtn"})
      face = choice(faces).attrs['data-clipboard-text']

      return face

    def __str__(self, **kwargs):
      return "Wanna see a fancy donger? Type me"

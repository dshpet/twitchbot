from .BaseCommand import BaseCommand
from urllib import request
from bs4 import BeautifulSoup
from random import choice
import json

class TwitchEmote(BaseCommand):
    """Gets a random twitch emote from twitchemotes api"""

    def perfrom(self, message, sender):
      raise RuntimeError("Not implemented")

    def respond(self, message, sender):
      url = "https://twitchemotes.com/api_cache/v2/global.json"
      response = request.urlopen(url).read()
      parsed = json.loads(response.decode('utf-8'))
      global_emotes = list(parsed['emotes'].keys())
      random_emote = choice(global_emotes)
      
      return "You are a " + random_emote + ", @" + sender

    def __str__(self, **kwargs):
      return "Wanna who you are? NO FAKE TWITCH TEST"


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .BaseCommand import BaseCommand
from urllib import request
import random
import json
import hashlib

class TwitchEmote(BaseCommand):
    """Gets a random twitch emote from twitchemotes api"""

    def respond(self, message, sender):
      url = "https://twitchemotes.com/api_cache/v3/global.json"
      response = request.urlopen(url).read()
      parsed = json.loads(response.decode('utf-8'))
      global_emotes = list(parsed.keys())

      hash = hashlib.md5(sender.encode()).hexdigest()
      random.seed(hash)
      random_emote = random.choice(global_emotes)
      
      return "You are a " + random_emote + ", @" + sender

    def __str__(self, **kwargs):
      return "Wanna who you are? NO FAKE TWITCH TEST"

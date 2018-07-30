#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .BaseCommand import BaseCommand
import wikipedia
import random

class Wikipedia(BaseCommand):
    """Gets a semi-random wikipedia article"""

    #
    # Config
    #
    
    number_of_sentences = 1

    #
    # Interface
    #

    def respond(self, message, sender):
      # api docs here
      # https://wikipedia.readthedocs.io/en/latest/code.html#api
      
      text = "Kappa"
      try:
        message_words = message.split() # remove duplicated whitespaces
        search_topic = None if len(message_words) == 1 else " ".join(message_words[1:]) # everything after command
        
        if search_topic == None or search_topic == "random" or search_topic == "rand":
          search_topic = wikipedia.random(pages=1)

        text = wikipedia.summary(search_topic, sentences = self.number_of_sentences)
     
      except wikipedia.DisambiguationError as e:
        print(e.options)
        first_definition = e.options[0] # more predictable
        random_definition = e.options[random.randrange(len(e.options))] # better in high amount

        text = wikipedia.summary(random_definition, sentences = self.number_of_sentences)
        
      except wikipedia.exceptions.PageError as e:
        print("No page found")
        text = sender + ", no page [ " + search_topic + "] found"

      return text

    def __str__(self, **kwargs):
      return "Wanna see a highly-educational piece of information? Usage !wiki topic (optional)"

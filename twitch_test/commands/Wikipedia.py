#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .BaseCommand import BaseCommand
import wikipedia

class Wikipedia(BaseCommand):
    """Gets a semi-random wikipedia article"""

    # UNCOMPLETED
    # TODO MESSAGE ARGS PROCESSING
    # TODO SAFE SUMMARY
    # https://wikipedia.readthedocs.io/en/latest/code.html#api
    def respond(self, message, sender):
      random_page_title = wikipedia.random(pages=1)
      text = wikipedia.summary(random_page_title, sentences = 1)

      try:
        search = wikipedia.search("Mercury", results=1, suggestion=True)
        first_result = search[0][0]
        suggestion = search[1]
        page = wikipedia.page(title = first_result)
        text = wikipedia.summary("zvvasdasdasdasd", sentences = 1)
      except wikipedia.DisambiguationError as e:
        print(e.options)
      except wikipedia.exceptions.PageError as e:
        print("ples")

      return text

    def __str__(self, **kwargs):
      return "Wanna see a highly-educational piece of information? DOIT"

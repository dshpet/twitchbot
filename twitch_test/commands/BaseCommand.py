#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class BaseCommand():
    """represents chat commands"""

    """
    command action

    returns string response to message from sender
    """
    def respond(self, message, sender):
      raise RuntimeError("Not implemented")

    """
    basic string representation acting as a helper to show purpose in chat
    """
    def __str__(self, **kwargs):
      raise RuntimeError("Not implemented")

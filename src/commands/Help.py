#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .BaseCommand import BaseCommand

class Help(BaseCommand):
    """basic help message for a chat user"""

    def basic_help(self):
      from .CommandsList import commands

      commands_string = "I recognize these commands for now: "

      for name, command in commands.items():
        commands_string = commands_string + " " + name

      advanced_usage = ". Use [!help topic] to get more info on command. Example: !help wiki"
      
      return commands_string + advanced_usage

    # kinda retarded function signature
    def help_on_topic(self, topics_list):
      from .CommandsList import commands

      command_name = topics_list[0]
      if command_name[0] != "!":
        command_name = "!" + command_name

      if command_name in commands:
        return "[ " + command_name + " ] " + str(commands[command_name])

      return "Command [" + command_name + "] not found"

    def respond(self, message, sender):
      words = message.split()[1:]
      if len(words) == 0:
        return self.basic_help()
      else:
        return self.help_on_topic(words)      

    def __str__(self, **kwargs):
      return "Use this command to show all available commands"

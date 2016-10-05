from .BaseCommand import BaseCommand

class Help(BaseCommand):
    """basic help message for a chat user"""

    def perfrom(self, message, sender):
      raise RuntimeError("Not implemented")

    def respond(self, message, sender):
      from .CommandsList import commands

      commands_string = "I recognize these commands for now: "

      for name, command in commands.items():
        commands_string = commands_string + name + " "

      return commands_string

    def __str__(self, **kwargs):
      return "Use this command to show all available commands"
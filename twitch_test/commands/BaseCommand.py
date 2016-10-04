class BaseCommand():
    """represents chat commands"""

    def perfrom(self, message, sender):
      raise RuntimeError("Not implemented")

    def respond(self, message, sender):
      raise RuntimeError("Not implemented")

    def __str__(self, **kwargs):
      raise RuntimeError("Not implemented")

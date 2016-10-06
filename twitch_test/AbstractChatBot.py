class AbstractChatBot(object):
  """Representation of an abstract chat bot. Main ideas - get response on certain message. 
     Incapsulates utility methods"""
  def __init__(self, **kwargs):
    raise RuntimeError("Not implemented")

  def send_message(self, message):
    raise RuntimeError("Not implemented")

  def process_message(self, message):
    raise RuntimeError("Not implemented")

  def start(self):
    raise RuntimeError("Not implemented")

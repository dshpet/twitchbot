from AbstractChatBot import AbstractChatBot

import socket
import re
from operator import methodcaller
import chatterbot

# helper util
encoding = 'UTF-8'
def str_to_byte(str):
  return bytes(str, encoding)

class TwitchBot(AbstractChatBot):
  """Actual twitch bot"""

  irc = socket.socket()
  host = "irc.twitch.tv"
  port = 6667
  chan = "#zersp"
  nick = "kappa_robot"
  pswd = "oauth:qdxk45u28g1qsx8rmnnacf2qgj9whb"
  chat_bot = None

  def __init__(self):
    self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connect(self.host, self.port, self.chan, self.nick)
    
    # TODO revisit bot config
    self.chat_bot = chatterbot.ChatBot(
      "KappaRobot", 
      storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
      logic_adapters=[
        "chatterbot.logic.MathematicalEvaluation",
        "chatterbot.logic.TimeLogicAdapter",
        "chatterbot.logic.ClosestMatchAdapter",
      ]
    )

    #self.chat_bot.set_trainer(chatterbot.trainers.ChatterBotCorpusTrainer)
    #self.chat_bot.train("chatterbot.corpus.english")

  #
  # IRC Commands
  #

  def send_message(self, message):
    self.irc.send(str_to_byte('PRIVMSG ' + self.chan + ' :' + message + '\r\n'))

  def send_pass(self):
    self.irc.send(str_to_byte('PASS ' + self.pswd + '\r\n'))

  def send_nick(self):
    self.irc.send(str_to_byte('NICK ' + self.nick + '\r\n'))

  def join_channel(self, channel):
    self.irc.send(str_to_byte('JOIN ' + channel + '\r\n'))

  def part_channel(self, channel):
    self.irc.send(str_to_byte('PART ' + channel + '\r\n'))

  def pong(self, message):
    self.irc.send(str_to_byte('PONG ' + message + '\r\n'))

  def connect(self, server, port, channel, botnick):
    print("connecting to: " + server + ":" + str(port))
    self.irc.connect((server, self.port))
    self.send_pass()
    self.send_nick()
    self.join_channel(self.chan)

  # getters
  def get_sender(self, line):
    message = line[0]
    sender, address = message[1:].split('!', 1)
    return sender

  def get_message(self, line):
    message = line[3][1:]
    for i in range(4, len(line)):
      message = message + " " + line[i]

    return message

  # commands and analyzers
  def process_message(self, message):    
   print(message)

   if message[0] == 'PING':
     self.pong('PONGERONI BACK')
     print('PONGERONI')
   
   if message[1] == 'PRIVMSG':
     sender = self.get_sender(message)
     message_text = self.get_message(message)
     
     self.do_command(message_text, sender)
   
     if ("@kappa_robot" in message_text):
       self.bot_process_message(message_text, sender)

  def do_command(self, message, sender):
    if message[0] != '!':
      return

    command = message.split(' ')[0] # first 

    from commands.CommandsList import commands
    if command in commands:
      self.send_message(commands[command].respond(message, sender))

  def bot_process_message(self, message, sender):
    message = re.sub('@kappa_robot', '', message) # remove name for sentence sanity
    message = re.sub(r"\s+", " ", message, flags=re.UNICODE) # remove whitespaces
    response = self.chat_bot.get_response(message)    
    
    self.send_message(response.text + " @" + sender)

  def start(self):
    data = ""
    while True:
      try:
        data = data + self.irc.recv(1024).decode(encoding)
        data_split = re.split(r"[~\r\n]+", data)
        data = data_split.pop() # dont save the whole history
    
        for line in data_split:
          line = str.strip(line)
          line = str.split(line)
    
          if len(line) == 0:
            break
    
          self.process_message(line)
    
      except socket.error:
        print("socket error")
    
      except socket.timeout:
        print("socket timeout")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from AbstractChatBot import AbstractChatBot

import socket
import re
import chatterbot
from operator import methodcaller

# Config
IS_LEARNING_ENABLED = False

# Utils TODO move to separate file

encoding = 'UTF-8'
endl     = "\r\n"

# Returns byte represenation to send through the network
def str_to_byte(str):
  return bytes(str, encoding)

class TwitchBot(AbstractChatBot):
  """
  Actual twitch bot

  For now it recognizes some commands and uses chatterbot as a free-speech response evaluator
  """
  #
  # Config
  #

  host            = "irc.twitch.tv"
  port            = 6667
  chan            = "#zersp"
  nick            = "kappa_robot"
  twitch_auth_key = b'\x9aA:\x8a!\xf0\x9e\xf5\xbc(\xc2\x0e\xf0Q\xe3\x87\xe4\xca1#\n\x94\x04ho\xc2d\x15\xc9Q\x99\x82,h\x18\xd7\xa7\x00\xa4,E\xffE\xab\x17B+\x8f'
  mongo_auth_key  = b'G\xcd-\x94\x18\xc9\xf2\xc2\x97\xdcS-`\xbaM<x\x9f\xb1S\xf2\xe7\x13&\xdc\x19\xfa\xc1\x98\x1f\x81\x94\x15J\xc7\xaf\xf1}\xc7<\xfe\x9a7*<\x1e\x8dL\xef\xa1\x1b\xf1k\x96\xf4\x82\xe7\xcaY\t\xa0\xe8+um&\xcd\xcb\xb7\xf0\xd4N\xf7\x98\x86^\xe6\xf0\xd8D'

  #
  # Members
  #

  irc             = socket.socket()
  chat_bot        = None

  #
  # Initialization
  #

  def decrypt_access_keys(self):
    from Crypto.Cipher import AES
    
    crypter = AES.new('76B305DACD6BE18BBF07F1DFB0C57E65', AES.MODE_ECB)

    self.twitch_auth_key = str(crypter.decrypt(self.twitch_auth_key).strip())[2:-1] # crop unnecessary braces and stuff
    self.mongo_auth_key  = str(crypter.decrypt(self.mongo_auth_key ).strip())[2:-1] # crop unnecessary braces and stuff

  def __init__(self):
    self.decrypt_access_keys()

    self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connect(self.host, self.port, self.chan, self.nick)
    
    self.chat_bot = chatterbot.ChatBot(
      name            = "KappaRobot", 
      storage_adapter = "chatterbot.storage.MongoDatabaseAdapter",
      database        = "twitch-chat-bot",
      database_uri    = self.mongo_auth_key,
      logic_adapters  = [
        {
            'import_path'     : 'chatterbot.logic.LowConfidenceAdapter',
            'threshold'       : 0.45,
            'default_response': "idk what you saying bruh"
        },
        {
            'import_path'                  : 'chatterbot.logic.BestMatch', # http://chatterbot.readthedocs.io/en/stable/logic/index.html
            'statement_comparison_function': 'chatterbot.comparisons.levenshtein_distance', # http://chatterbot.readthedocs.io/en/stable/conversations.html#statement-comparison
            'response_selection_method'    : 'chatterbot.response_selection.get_most_frequent_response' # http://chatterbot.readthedocs.io/en/stable/logic/response_selection.html#response-selection
        },
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation'
        },
        {
            'import_path': 'chatterbot.logic.TimeLogicAdapter'
        }
      ]
    )

    if IS_LEARNING_ENABLED:
      print("Initial learning process started...")
      self.chat_bot.set_trainer(chatterbot.trainers.ChatterBotCorpusTrainer)

      self.chat_bot.train("chatterbot.corpus.english")
      self.chat_bot.train("chatterbot.corpus.russian")
      self.chat_bot.train("chatterbot.corpus.chinese")
      self.chat_bot.train("chatterbot.corpus.french")
      self.chat_bot.train("chatterbot.corpus.german")
      self.chat_bot.train("chatterbot.corpus.hindi")
      self.chat_bot.train("chatterbot.corpus.indonesia")
      self.chat_bot.train("chatterbot.corpus.italian")
      self.chat_bot.train("chatterbot.corpus.marathi")
      self.chat_bot.train("chatterbot.corpus.portuguese")
      self.chat_bot.train("chatterbot.corpus.spanish")
      self.chat_bot.train("chatterbot.corpus.telugu")

      print("Initial learning process finished")

  #
  # IRC Commands
  #

  def send_message(self, message):
    self.irc.send(str_to_byte('PRIVMSG ' + self.chan + ' :' + message + endl))

  def send_pass(self):
    self.irc.send(str_to_byte('PASS ' + self.twitch_auth_key + endl))

  def send_nick(self):
    self.irc.send(str_to_byte('NICK ' + self.nick + endl))

  def join_channel(self, channel):
    self.irc.send(str_to_byte('JOIN ' + channel + endl))

  def part_channel(self, channel):
    self.irc.send(str_to_byte('PART ' + channel + endl))

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
   
     if (("@" + self.nick) in message_text):
       self.bot_process_message(message_text, sender)

  def do_command(self, message, sender):
    if message[0] != '!':
      return

    command = message.split(' ')[0] # first 

    from commands.CommandsList import commands
    if command in commands:
      self.send_message(commands[command].respond(message, sender))

  def bot_process_message(self, message, sender):
    message = re.sub(("@" + self.nick), '', message) # remove name for sentence sanity
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

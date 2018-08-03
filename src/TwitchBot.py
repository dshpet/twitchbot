#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import re
import random
from operator import methodcaller
import threading
import asyncio

# todo this
# from twitch import TwitchClient
# client = TwitchClient(client_id='ve8viepd4zb5kwlxri8aoxtgce2bad', oauth_token='esgjiuok1leqoay8l91pkiynun4su1')
# channels = client.search.channels('zersp', limit=69, offset=420)
# channel = client.channels.get()
# 
# print(channel.id)
# print(channel.name)
# print(channel.display_name)

import sys
sys.path.insert(0, './utils')
sys.path.insert(0, '.')
import StringUtils
import IRCClient

class TwitchBot():
  #
  # Config
  #

  host            = "irc.chat.twitch.tv"
  port            = 6667
  channel         = "zersp"
  nickname        = "kappa_robot"
  twitch_auth_key = b'\x9aA:\x8a!\xf0\x9e\xf5\xbc(\xc2\x0e\xf0Q\xe3\x87\xe4\xca1#\n\x94\x04ho\xc2d\x15\xc9Q\x99\x82,h\x18\xd7\xa7\x00\xa4,E\xffE\xab\x17B+\x8f'
  mongo_auth_key  = b'G\xcd-\x94\x18\xc9\xf2\xc2\x97\xdcS-`\xbaM<x\x9f\xb1S\xf2\xe7\x13&\xdc\x19\xfa\xc1\x98\x1f\x81\x94\x15J\xc7\xaf\xf1}\xc7<\xfe\x9a7*<\x1e\x8dL\xef\xa1\x1b\xf1k\x96\xf4\x82\xe7\xcaY\t\xa0\xe8+um&\xcd\xcb\xb7\xf0\xd4N\xf7\x98\x86^\xe6\xf0\xd8D'

  #
  # Members
  #

  # check for better typename strategy
  main_loop = asyncio.BaseEventLoop
  irc       = IRCClient.IRCClient
  chat_data = str

  #
  # Initialization
  #

  def __init__(self):
    self.decrypt_access_keys()
    self.chat_data = ""

  def decrypt_access_keys(self):
    from Crypto.Cipher import AES
    
    crypter = AES.new('76B305DACD6BE18BBF07F1DFB0C57E65', AES.MODE_ECB)

    self.twitch_auth_key = str(crypter.decrypt(self.twitch_auth_key).strip())[2:-1] # crop unnecessary braces and stuff
    self.mongo_auth_key  = str(crypter.decrypt(self.mongo_auth_key ).strip())[2:-1] # crop unnecessary braces and stuff

  def start(self):
    self.irc = IRCClient.IRCClient(self.channel, self.nickname, self.twitch_auth_key, self.host, self.port)
    print("Started successfully")

  #
  # Commands/Analyzers
  #

  def process_message(self, message):
   if message[0] == 'PING': # todo move and return only meaningful data
     self.irc.pong('PONGERONI BACK')
     print('PONGERONI')
   
   if message[1] == 'PRIVMSG':
     sender = StringUtils.get_sender(message)
     message_text = StringUtils.get_message(message)

     print(sender + ":" + message_text)
     
     self.do_command(message_text, sender)

  def do_command(self, message, sender):
    if message[0] != '!':
      return

    command = message.split(' ')[0] # first 

    from commands.CommandsList import commands
    if command in commands:
      self.send_message(commands[command].respond(message, sender))

  def generate_random_message(self): # todo rethink
    print("generate_random_message")
    random_viewer = random.choice(self.get_users())
    from commands.CommandsList import commands # remove help
    random_command = random.choice(list(commands.keys())) # uuuuh
    self.send_message(commands[random_command].respond("ololo", random_viewer))

  def receive_data(self): # todo maybe move to IRC
    try:
      self.chat_data = self.chat_data + self.irc.get_data()
      if (self.chat_data is not ""):
        print(self.chat_data)

    except Exception as e:
      print(str(e))
  
  def process_messages(self): # todo maybe separate with IRC
    data_split = re.split(r"[~\r\n]+", self.chat_data)    
    for line in data_split:
      line = str.strip(line)
      line = str.split(line)
    
      if len(line) == 0:
        break
    
      self.process_message(line)

    self.chat_data = ""

  def update(self):
    # todo async
    self.receive_data()
    self.process_messages()

    #if random.randint(0, 100) < 69:
    # print("before message generation")
    # # self.generate_random_message() # todo check why is not called sometimes
    # print("after message generation")
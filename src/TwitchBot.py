#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import re
import random
from operator import methodcaller

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
import StringUtils

class TwitchBot():
  #
  # Config
  #

  host            = "irc.chat.twitch.tv"
  port            = 6667
  channel         = "#zersp"
  nickname        = "kappa_robot"
  twitch_auth_key = b'\x9aA:\x8a!\xf0\x9e\xf5\xbc(\xc2\x0e\xf0Q\xe3\x87\xe4\xca1#\n\x94\x04ho\xc2d\x15\xc9Q\x99\x82,h\x18\xd7\xa7\x00\xa4,E\xffE\xab\x17B+\x8f'
  mongo_auth_key  = b'G\xcd-\x94\x18\xc9\xf2\xc2\x97\xdcS-`\xbaM<x\x9f\xb1S\xf2\xe7\x13&\xdc\x19\xfa\xc1\x98\x1f\x81\x94\x15J\xc7\xaf\xf1}\xc7<\xfe\x9a7*<\x1e\x8dL\xef\xa1\x1b\xf1k\x96\xf4\x82\xe7\xcaY\t\xa0\xe8+um&\xcd\xcb\xb7\xf0\xd4N\xf7\x98\x86^\xe6\xf0\xd8D'

  #
  # Members
  #

  irc       = socket.socket()
  chat_data = ""

  #
  # Initialization
  #

  def __init__(self):
    self.decrypt_access_keys()

  def decrypt_access_keys(self):
    from Crypto.Cipher import AES
    
    crypter = AES.new('76B305DACD6BE18BBF07F1DFB0C57E65', AES.MODE_ECB)

    self.twitch_auth_key = str(crypter.decrypt(self.twitch_auth_key).strip())[2:-1] # crop unnecessary braces and stuff
    self.mongo_auth_key  = str(crypter.decrypt(self.mongo_auth_key ).strip())[2:-1] # crop unnecessary braces and stuff

  def start(self):
    self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connect(self.host, self.port, self.channel, self.nickname)
    self.chat_data = ""

    print("Started successfully")

  #
  # IRC Commands
  #

  # todo move
  def send_message(self, message):
    self.irc.send(StringUtils.str_to_byte('PRIVMSG ' + self.channel + ' :' + message + StringUtils.endl))

  def send_pass(self):
    self.irc.send(StringUtils.str_to_byte('PASS ' + self.twitch_auth_key + StringUtils.endl))

  def send_nick(self):
    self.irc.send(StringUtils.str_to_byte('NICK ' + self.nickname + StringUtils.endl))

  def join_channel(self, channel):
    self.irc.send(StringUtils.str_to_byte('JOIN ' + channel + StringUtils.endl))

  def part_channel(self, channel):
    self.irc.send(StringUtils.str_to_byte('PART ' + channel + StringUtils.endl))

  def pong(self, message):
    self.irc.send(StringUtils.str_to_byte('PONG ' + message + StringUtils.endl))

  def connect(self, server, port, channel, botnick):
    print("connecting to: " + server + ":" + str(port))
    self.irc.connect((server, self.port))
    self.send_pass()
    self.send_nick()
    self.join_channel(self.channel)

  #
  # Commands/Analyzers
  #

  def process_message(self, message):
   if message[0] == 'PING':
     self.pong('PONGERONI BACK')
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
    random_viewer = 'zersp' # todo
    from commands.CommandsList import commands # remove help
    random_command = random.choice(list(commands.keys())) # uuuuh
    self.send_message(commands[random_command].respond("ololo", random_viewer))
    

  def receive_data(self):
    try:
      self.chat_data = self.chat_data + self.irc.recv(1024).decode(StringUtils.main_encoding)

    except Exception as e:
      print(str(e))
  
  def process_messages(self):
    data_split = re.split(r"[~\r\n]+", self.chat_data)    
    for line in data_split:
      line = str.strip(line)
      line = str.split(line)
    
      if len(line) == 0:
        break
    
      self.process_message(line)

    self.chat_data = ""

  def update(self):
    # todo monitor load between receiving and processing
    self.receive_data()
    self.process_messages()

    if random.randint(0, 100) < 69:
      self.generate_random_message()
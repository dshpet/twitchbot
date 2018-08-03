#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import asyncio
import json
from urllib import request

import sys
sys.path.insert(0, './utils')
import StringUtils

class IRCClient():

  irc_socket = None
  channel    = None
  nickname   = None
  password   = None

  def __init__(self, _channel : str, _nickname : str, _password : str, _host = "irc.chat.twitch.tv", _port = 6667):
    self.channel  = _channel 
    self.nickname = _nickname
    self.password = _password

    print("connecting to: " + str(_host) + ":" + str(_port))
    self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.irc_socket.connect((_host, _port))
    self.send_password(self.password)
    self.send_nickname(self.nickname)
    self.join_channel(self.channel)

  def send_message(self, _message : str) -> None:
    self.irc_socket.send(StringUtils.str_to_byte('PRIVMSG ' + '#' + self.channel + ' :' + _message + StringUtils.endl))

  def send_password(self, _password : str) -> None:
    self.irc_socket.send(StringUtils.str_to_byte('PASS ' + _password + StringUtils.endl))

  def send_nickname(self, _nickname : str) -> None:
    self.irc_socket.send(StringUtils.str_to_byte('NICK ' + _nickname + StringUtils.endl))

  def join_channel(self, _channel : str) -> None:
    self.irc_socket.send(StringUtils.str_to_byte('JOIN ' + '#' + _channel + StringUtils.endl))

  def part_channel(self, _channel : str) -> None:
    self.irc_socket.send(StringUtils.str_to_byte('PART ' + '#' + _channel + StringUtils.endl))

  def pong(self, _message : str) -> None:
    self.irc_socket.send(StringUtils.str_to_byte('PONG ' + _message + StringUtils.endl))

  def get_data(self) -> str:
    return self.irc_socket.recv(1024).decode(StringUtils.main_encoding)

  # needs some rework as it stops receiving data when chat is not moving
  async def get_data_async(self) -> str:
    return await self.irc_socket.recv(1024).decode(StringUtils.main_encoding)

  def get_users(self):
    url = 'http://tmi.twitch.tv/group/user/' + self.channel + '/chatters'
    response = request.urlopen(url).read()
    parsed = json.loads(response.decode(StringUtils.main_encoding))
    chatters = parsed['chatters']

    admins      = chatters['admins']
    global_mods = chatters['global_mods']
    moderators  = chatters['moderators']
    staff       = chatters['staff']
    viewers     = chatters['viewers']
    all_viewers = admins + global_mods + moderators + staff + viewers
    
    return all_viewers

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import re
import random
from operator import methodcaller
import threading
import asyncio

import sys
sys.path.insert(0, './utils')
import StringUtils

class IRCClient():

  irc_socket = None
  channel    = None
  nickname   = None
  password   = None
  host

  def __init__(self, _channel : str, _nickname : str, _password : str, _host = "irc.chat.twitch.tv", _port = 6667):
    self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.irc_socket.create_connection((_host, _port))

    self.channel  = _channel 
    self.nickname = _nickname
    self.password = _password

  def send_message(self, message : str) -> None:
    self.irc_socket.send(StringUtils.str_to_byte('PRIVMSG ' + '#' + self.channel + ' :' + message + StringUtils.endl))

  def send_pass(self) -> None:
    self.irc_socket.send(StringUtils.str_to_byte('PASS ' + self.password + StringUtils.endl))

  def send_nick(self) -> None:
    self.irc_socket.send(StringUtils.str_to_byte('NICK ' + self.nickname + StringUtils.endl))

  def join_channel(self, channel : str) -> None:
    self.irc_socket.send(StringUtils.str_to_byte('JOIN ' + '#' + channel + StringUtils.endl))

  def part_channel(self, channel : str) -> None:
    self.irc_socket.send(StringUtils.str_to_byte('PART ' + '#' + channel + StringUtils.endl))

  def pong(self, message : str) -> None:
    self.irc_socket.send(StringUtils.str_to_byte('PONG ' + message + StringUtils.endl))

  # needs some rework as it stops receiving data when chat is not moving
  async def get_data(self) -> str:
    return await self.irc.recv(1024).decode(StringUtils.main_encoding)

  def connect(self, server, port, channel, botnick):
    print("connecting to: " + self.irc_socket. + ":" + str(port))
    self.irc.connect((server, self.port))
    self.send_pass()
    self.send_nick()
    self.join_channel(self.channel)

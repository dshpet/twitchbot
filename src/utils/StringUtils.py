#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Constants
#

main_encoding = 'UTF-8'
endl          = "\r\n"

#
# Common
#

# Returns byte represenation to send through the network
def str_to_byte(string : str) -> str:
  return bytes(string, main_encoding)

#
# Twitch specific
#

def get_sender(irc_line : str) -> str:
  sender, address = irc_line[0][1:].split('!', 1)
  return sender

def get_message(irc_line : str) -> str:
  message = irc_line[3][1:]
  for i in range(4, len(irc_line)): # wtf
    message = message + " " + irc_line[i]

  return message
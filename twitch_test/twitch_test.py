# import irc
import socket
import sys

encoding = 'UTF-8'
def str_to_byte(str):
  return bytes(str, encoding)

class TwitchChat:
  
  # Kappa
  irc = socket.socket()
  host = "irc.twitch.tv"
  port = 6667
  
  def __init__(self):
    self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connect(self.host, self.port, self.chan, self.nick)

  def send(self, message):
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
  
twitch = TwitchChat()
twitch.send(twitch.chan, "nice")

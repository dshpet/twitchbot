# import irc
import socket
import sys
import re
from operator import methodcaller

encoding = 'UTF-8'
def str_to_byte(str):
  return bytes(str, encoding)

class TwitchChat:
  
  # Kappa
  irc = socket.socket()
  host = "irc.twitch.tv"
  port = 6667
  chan = "#zersp"
  nick = "kappa_robot"
  pswd = "oauth:qdxk45u28g1qsx8rmnnacf2qgj9whb"
  
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

  # getters
  def get_sender(self, line):
    message = line[0]
    sender, address = message[1:].split('!', 1)
    return sender

  def get_message(self, line):
    message = line[3][1:]
    return message

  # commands and analyzers
  def do_command(self, line):
    message = self.get_message(line)
    sender = self.get_sender(line)

    if message[0] != '!':
      return

    command = message.split(' ')[0] # first 
    if command in self.commands:
      self.commands[command](self)

  def command_kappa(self):
    self.send("Kappa")

  commands = {
    '!Kappa': command_kappa
  }
    
    
  
twitch = TwitchChat()
twitch.send("fuck")


data = ""
while True:
  try:
    data = data + twitch.irc.recv(1024).decode(encoding)
    data_split = re.split(r"[~\r\n]+", data)
    data = data_split.pop() # dont save the whole history

    for line in data_split:
      line = str.strip(line)
      line = str.split(line)

      if len(line) == 0:
        break

      if line[0] == 'PING':
        twitch.pong()
        print('PONGERONI')

      if line[1] == 'PRIVMSG':
        sender = twitch.get_sender(line)
        message = twitch.get_message(line)
        twitch.do_command(line)        

        twitch.send('hey, fuck you ' + sender)

  except socket.error:
    print("socket error")

  except socket.timeout:
    print("socket timeout")

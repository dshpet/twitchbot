# import irc
import socket
import sys
import re
from operator import methodcaller
from urllib import request
from bs4 import BeautifulSoup
from random import choice
import json

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
  commands = {}
  
  def __init__(self):
    self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connect(self.host, self.port, self.chan, self.nick)
    self.init_commands()
    
  # todo move to separate entity
  def init_commands(self):
      self.commands = {
        '!help': self.command_help,
        '!bot': self.command_kappa,
        '!pasta' : self.command_random_pasta,
        '!ascii' : self.command_ascii,
        '!face' : self.command_donger_face,
        '!myemote' : self.random_emote
      }

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
      self.commands[command](sender)

  def command_kappa(self, sender):
    self.send("Kappa")

  def command_help(self, sender):
    commands_string = "I recognize these commands for now: "
    for command, action in self.commands.items():
      commands_string = commands_string + command + " "
  
    self.send(commands_string)

  def command_random_pasta(self, sender):
    pasta_site = request.urlopen("http://www.twitchquotes.com/random") # ty for pastas bois
    pasta_doc = pasta_site.read()
    soup = BeautifulSoup(pasta_doc, 'html.parser')
    real_pasta = soup.find(id="quote_content_1")
    pasta_text = str(real_pasta.contents[0]) # i don't like it but for simple purposes it works
    self.send(pasta_text)

  def command_ascii(self, sender):
    pasta_site = request.urlopen("http://www.twitchquotes.com/copypastas/ascii-art")
    pasta_doc = pasta_site.read()
    soup = BeautifulSoup(pasta_doc, 'html.parser')
    all_links = soup.find_all('a', {"class":"ascii_preview_link"})

    ascii_site = request.urlopen("http://www.twitchquotes.com/" + choice(all_links).attrs['href'])
    ascii_doc = ascii_site.read()
    ascii_soup = BeautifulSoup(ascii_doc, 'html.parser')
    art = ascii_soup.find(id = 'quote_content_0')
    self.send(art.contents[0])

  def command_donger_face(self, sender):
    url = "http://textfac.es"
    req = request.Request(url, headers={'User-Agent' : "Magic Browser"}) # blockers DansGame
    pasta_site = request.urlopen(req)
    pasta_doc = pasta_site.read()
    soup = BeautifulSoup(pasta_doc, 'html.parser')
    faces = soup.find_all('button', {"class":"facebtn"})
    face = choice(faces).attrs['data-clipboard-text']
    self.send(face)

  def random_emote(self, sender):
    url = "https://twitchemotes.com/api_cache/v2/global.json"
    response = request.urlopen(url).read()
    parsed = json.loads(response.decode('utf-8'))
    global_emotes = list(parsed['emotes'].keys())
    random_emote = choice(global_emotes)
    self.send("You are a " + random_emote + ", @" + sender)    
 
twitch = TwitchChat()
twitch.send("I AM ALIVE!!!!")


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
        twitch.pong('PONGERONI BACK')
        print('PONGERONI')

      if line[1] == 'PRIVMSG':
        sender = twitch.get_sender(line)
        message = twitch.get_message(line)
        twitch.do_command(line)        

        #twitch.send('hey, fuck you ' + sender)

  except socket.error:
    print("socket error")

  except socket.timeout:
    print("socket timeout")

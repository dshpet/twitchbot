#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main():
  from TwitchBot import TwitchBot
  from commands.Wikipedia import Wikipedia

  twitch = TwitchBot()
  twitch.start()
  while True:
    twitch.update()

if __name__ == "__main__":
  main()
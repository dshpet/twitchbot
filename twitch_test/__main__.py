#!usr/bin/env/python

from TwitchBot import TwitchBot
 
def main():
  twitch = TwitchBot()
  twitch.send_message("I AM ALIVE!!!")
  twitch.start()

if __name__ == "__main__":
  main()
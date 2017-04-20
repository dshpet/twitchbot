#!usr/bin/env/python

def main():
  from TwitchBot import TwitchBot 

  twitch = TwitchBot()
  twitch.send_message("I AM ALIVE!!!")
  twitch.start()

if __name__ == "__main__":
  main()
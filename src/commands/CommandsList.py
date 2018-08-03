#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .Help import Help
from .DongerFace import DongerFace
from .RandomPasta import RandomPasta
from .AsciiArt import AsciiArt
from .TwitchEmote import TwitchEmote
from .Wikipedia import Wikipedia

commands = {
  #'!help'    : Help(),
  #'!pasta'   : RandomPasta(),
  #'!ascii'   : AsciiArt(),
  #'!face'    : DongerFace(),
  '!myemote' : TwitchEmote(),
  #'!wiki'    : Wikipedia()
}

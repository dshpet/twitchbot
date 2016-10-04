from .Help import Help
from .DongerFace import DongerFace
from .RandomPasta import RandomPasta
from .AsciiArt import AsciiArt
from .TwitchEmote import TwitchEmote

commands = {
  '!help': Help(),
  '!pasta' : RandomPasta(),
  '!ascii' : AsciiArt(),
  '!face' : DongerFace(),
  '!myemote' : TwitchEmote()
}

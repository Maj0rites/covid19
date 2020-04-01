import dbl
import discord
from discord.ext import commands
import config

class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = config.dbl_token # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True) # Autopost will post your guild count every 30 minutes

def setup(bot):
    bot.add_cog(TopGG(bot))

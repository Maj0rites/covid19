  
import discord
import os
import config
import asyncio
import logging
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler
from discord.utils import find
from discord.ext import commands
from discord.ext.commands import when_mentioned_or
from datetime import datetime

logging_client = google.cloud.logging.Client()
cloud_logger = logging_client.logger('covid-19')
logger = logging.getLogger('covid-19')
logger.setLevel(logging.DEBUG)
handler = CloudLoggingHandler(logging_client)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class Coronavirus(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=when_mentioned_or('.c '),
            activity=discord.Game(name="Loading...")
            )
        self.remove_command('help')
        self.load()

    def load(self):
        for filename in os.listdir('./cogs'):
            try:
                if filename.endswith('.py'):
                    self.load_extension(f'cogs.{filename[:-3]}')
                    logger.info(f'{filename} loaded successfully')
            except Exception:
                logger.exception(f'{filename} failed to load')

    def unload(self):
        for filename in os.listdir('./cogs'):
            try:
                if filename.endswith('.py'):
                    self.unload_extension(f'cogs.{filename[:-3]}')
                    logger.info(f'{filename} unloaded successfully')
            except Exception:
                logger.exception(f'{filename} failed to unload')

    async def on_ready(self):
        await self.wait_until_ready()
        while True:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{len(bot.guilds)} servers | .c help'))
            self.unload_extension('cogs.Stats')
            self.load_extension('cogs.Stats')
            logger.info('Reloaded Stats')
            await asyncio.sleep(600)

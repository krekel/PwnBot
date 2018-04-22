import config
import discord
import logging
import aiohttp

from discord.ext import commands

logging.basicConfig(filename='server.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), pm_help=True)

# COGS
bot.load_extension('cogs.web_crawler')
bot.load_extension('cogs.info')


@bot.event
async def on_ready():
    bot.session = aiohttp.ClientSession(loop=bot.loop)
    print('Bot ready')


@bot.event
async def on_message(message):
    # Bot messages will not be logged
    if message.author.bot:
        pass
    else:
        logger.info(f'AUTHOR: {message.author}, CHANNEL: {message.channel}, CONTENT: {message.content}')
        await bot.process_commands(message)


@bot.command()
async def ping(ctx):
    await ctx.send('Pong')


bot.run(config.TOKEN)

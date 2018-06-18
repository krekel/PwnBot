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
bot.load_extension('cogs.api')
# bot.load_extension('cogs.info')
bot.load_extension('cogs.poll')
bot.load_extension('cogs.tools')


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
        logger.info(f'AUTHOR: {message.author}, CHANNEL: {message.channel}, CONTENT: {message.content}'.encode('utf-8'))
        await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'Missing arguments for {ctx.command}')
    elif isinstance(error, commands.CommandNotFound):
        pass
    # TODO finish error handling


@bot.command()
async def ping(ctx):
    await ctx.send('Pong')


bot.run(config.TOKEN)

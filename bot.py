import config
from discord.ext import commands


class PwnBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), pm_help=True)
        self.token = config.TOKEN

    async def on_ready(self):
        print('Bot ready')

bot = PwnBot()
bot.run(bot.token)
